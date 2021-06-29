from validate_email import validate_email 
from variaveis import *
from src.functions import *
from src.database import *

#Busca as pessoas com data de nascimento maior que data de admissão
def pessoa_data_nascimento_maior_data_admissao():

    resultado = select(
        """
            SELECT 
                i_funcionarios,
                i_entidades,
                f.dt_admissao,
                pf.dt_nascimento,
                pf.i_pessoas,
                p.nome
            FROM 
                bethadba.funcionarios f
            INNER JOIN 
                bethadba.pessoas_fisicas pf ON (f.i_pessoas = pf.i_pessoas)
            INNER JOIN 
                bethadba.pessoas p ON (f.i_pessoas = p.i_pessoas)
            WHERE
                pf.dt_nascimento > f.dt_admissao;
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return

    print('Pessoas com data de nascimento maior que data de admissão: '+ str(quantidade))

#Busca a data de vencimento da CNH menor que a data de emissão da 1ª habilitação!
def pessoa_data_vencimento_cnh_menor_data_emissao():

    resultado = select(
        """
            SELECT 
                pessoas_fis_compl.i_pessoas
            FROM   
                bethadba.pessoas_fis_compl
            WHERE  
                dt_primeira_cnh > dt_vencto_cnh;
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return

    print('Pessoas com data de vencimento da CNH maior que emissão da 1ª habilitação: '+ str(quantidade))

    return quantidade

#Busca pessoas com data de nascimento maior que emissão da 1ª habilitação!
def pessoaDataVencimentoCNHMaiorNascimento():

    resultado = select(
        """
            SELECT i_pessoas,
                    (SELECT a.dt_nascimento
                FROM   
                    bethadba.pessoas_fisicas AS a
                WHERE  
                    a.i_pessoas = hpf.i_pessoas) nascimento,
                dt_emissao_cnh,
                NULL AS novaDataCNH
            FROM   
                bethadba.pessoas_fis_compl hpf
            WHERE  
                nascimento >= dt_primeira_cnh; 
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Pessoas com data de nascimento maior que emissão da 1ª habilitação: '+ str(quantidade))

    return quantidade    

#Busca os campos adicionais com descrição repetido
def campoAdicionalDescricaoRepetido():

    resultado = select(
        """
           SELECT 
                LIST(i_caracteristicas), 
                TRIM(nome), 
                COUNT(nome) 
            FROM 
                bethadba.caracteristicas 
            GROUP BY 
                TRIM(nome) 
            HAVING 
                COUNT(nome) > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Campos adicionais com descrição repetido: '+ str(quantidade))

    return quantidade

#Verifica se o dependente está cadastrado como 10 - OUTROS
def dependentesOutros():

    resultado = select(
        """
            SELECT 
                i_dependentes,
                i_pessoas
            FROM
                bethadba.dependentes,
            WHERE 
                grau = 10
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Dependentes cadastrados como OUTROS: '+ str(quantidade))

    return quantidade

#Pessoas com data de nascimento nulo
def pessoaDataNascimentoNulo():

    resultado = select(
        """
            SELECT 
                p.i_pessoas,
                p.nome,
                pf.dt_nascimento 
            FROM
                bethadba.pessoas p, 
                bethadba.pessoas_fisicas pf  
            WHERE 
                dt_nascimento IS NULL 
                AND p.i_pessoas = pf.i_pessoas
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Pessoas com data de nascimento nulo: '+ str(quantidade))

    return quantidade

#Pessoas com data de nascimento maior que data de dependencia
def pessoaDataNascimentoMaiorDataDependecia():

    resultado = select(
        """
            SELECT 
                d.i_dependentes,
                pf.dt_nascimento,
                d.dt_ini_depende 
            FROM 
                bethadba.dependentes d 
            JOIN 
                bethadba.pessoas_fisicas pf  ON (d.i_dependentes = pf.i_pessoas)
            WHERE 
                dt_nascimento > dt_ini_depende
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Pessoas com data de nascimento maior do que data de dependencia: '+ str(quantidade))

    return quantidade

#Pessoas com data de nascimento maior que data de nascimento do responsavel
def pessoaDataNascimentoMaiorDataNascimentoResponsavel():

    resultado = select(
        """
            SELECT 
                pf.i_pessoas as idPai,
                dt_nascimento as dataNascimentoPai, 
                i_dependentes as idFilho, 
                (
                    SELECT 
                        a.dt_nascimento 
                    FROM 
                        bethadba.pessoas_fisicas a 
                    WHERE 
                        a.i_pessoas = d.i_dependentes
                ) AS dataNascimentoFilho 
            FROM 
                bethadba.pessoas_fisicas pf 
            INNER JOIN 
                bethadba.dependentes d ON (pf.i_pessoas = d.i_pessoas)
            WHERE 
                dataNascimentoFilho < dataNascimentoPai 
                OR dataNascimentoFilho IS NULL
                AND grau = 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Pessoas com data de nascimento maior do que data de nascimento do responsavel: '+ str(quantidade))

    return quantidade

#Verifica os CPF's nulos
def cpfNulo():

    resultado = select(
        """
            SELECT 
                p.i_pessoas,
                p.nome
            FROM 
                bethadba.pessoas p, 
                bethadba.pessoas_fisicas pf  
            WHERE 
                cpf IS NULL AND 
                p.i_pessoas = pf.i_pessoas     
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('CPF nulo(s): '+ str(quantidade))

    return quantidade

#Verifica os CPF's repetidos
#As Pessoas (0,0) possuem o mesmo CPF!
def cpfRepetido():

    resultado = select(
        """
            SELECT
                list(pf.i_pessoas),
                cpf,
                count(cpf) AS quantidade
            FROM 
                bethadba.pessoas_fisicas pf 
            GROUP BY 
                cpf 
            HAVING 
                quantidade > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('CPF repetido(s): '+ str(quantidade))

    return quantidade

#Verifica os PIS's repetidos
#As Pessoas (0,0) possuem o mesmo número do PIS!
def pisRepetido():

    resultado = select(
        """
            SELECT
                list(pf.i_pessoas),
                num_pis,
                count(num_pis) AS quantidade
            FROM 
                bethadba.pessoas_fisicas pf 
            GROUP BY 
                num_pis 
            HAVING 
                quantidade > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('PIS repetido(s): '+ str(quantidade))

    return quantidade

#Verifica se o PIS é valido
#PIS inválido
def pisInvalido():

    resultado = select(
        """
           SELECT
                i_pessoas,
                num_pis
            FROM 
                bethadba.pessoas_fisicas
            WHERE 
                num_pis IS NOT NULL;
        """
    )

    quantidade = 0

    for i in resultado:
        pis = i[1]

        if not validarPis(pis):
            quantidade += 1

    if quantidade == 0:
        return 0

    print('PIS invalido(s): '+ str(quantidade))

    return quantidade

#Verifica os PIS's repetidos
def cnpjNulo():

    resultado = select(
        """
            SELECT 
                pj.i_pessoas,
                p.nome
            FROM 
                bethadba.pessoas_juridicas pj 
            INNER JOIN 
                bethadba.pessoas p ON (pj.i_pessoas = p.i_pessoas)
            WHERE 
                cnpj IS NULL
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('CNPJ nulo(s): '+ str(quantidade))

    return quantidade

#Verifica a descrição dos logradouros que tem caracter especial no inicio da descrição
def logradourosDescricaoCaracterEspecial():

    resultado = select(
        """
            SELECT 
                SUBSTRING(nome, 1, 1) as nome_com_caracter 
            FROM 
                bethadba.ruas 
            WHERE 
                nome_com_caracter in ('[', ']')
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Logradouros que tem caracter especial no inicio da descrição: '+ str(quantidade))

    return quantidade

#Verifica os logradouros com descrição repetidos
def logradourosDescricaoRepetido():

    resultado = select(
        """
            SELECT 
                list(i_ruas), 
                TRIM(nome),
                i_cidades, 
                count(nome) AS quantidade
            FROM 
                bethadba.ruas 
            GROUP BY 
                TRIM(nome), 
                i_cidades
            HAVING 
                quantidade > 1;
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Logradouros repetido(s): '+ str(quantidade))

    return quantidade

#Renomeia os tipos bases repetidos
def tiposBasesRepetido():

    resultado = select(
        """
            SELECT 
                list(i_tipos_bases), 
                nome, 
                count(nome) AS quantidade
            FROM 
                bethadba.tipos_bases 
            GROUP BY 
                nome 
            HAVING 
                quantidade > 1;
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Tipos bases repetido(s): '+ str(quantidade))

    return quantidade

#Verifica os logradouros sem cidades
def logradourosSemCidade():

    resultado = select(
        """
            SELECT 
                i_ruas,
                nome
            FROM 
                bethadba.ruas 
            WHERE 
                i_cidades IS NULL
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Logradouros sem cidade(s): '+ str(quantidade))

    return quantidade

#Verifica os atos com número nulos
def atosNumeroNulo():

    resultado = select(
        """
            SELECT 
                i_atos
            FROM 
                bethadba.atos 
            WHERE
                num_ato IS NULL OR num_ato = '';   
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Atos com número nulo: '+ str(quantidade))

    return quantidade

#Verifica os atos repetidos
def atosRepetido():

    resultado = select(
        """
            SELECT 
                list(i_atos),
                num_ato,
                i_tipos_atos,
                count(num_ato) AS quantidade
            FROM 
                bethadba.atos 
            GROUP BY 
                num_ato,
                i_tipos_atos 
            HAVING 
                quantidade > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Atos repetido(s): '+ str(quantidade))

    return quantidade

#Verifica os CBO's nulos nos cargos
def cargoCboNulo():

    resultado = select(
        """
            SELECT 
                * 
            FROM 
                bethadba.cargos 
            WHERE 
                i_cbo IS NULL
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('CBO do cargo nulo(s): '+ str(quantidade))

    return quantidade

#Verifica categoria eSocial nulo no vinculo empregaticio
def eSocialNuloVinculoEmpregaticio():

    resultado = select(
        """
            SELECT 
                i_vinculos,
                descricao,
                categoria_esocial
            FROM 
                bethadba.vinculos
            WHERE 
                categoria_esocial IS NULL
                AND tipo_func <> 'B'  
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('eSocial nulo nos vinculos empregraticios: '+ str(quantidade))

    return quantidade

#Renomeia os vinculos empregaticios repetidos
def vinculoEmpregaticioRepetido():

    resultado = select(
        """
            SELECT 
                list(i_vinculos), 
                descricao,
                count(descricao) AS quantidade 
            FROM 
                bethadba.vinculos 
            GROUP BY 
                descricao 
            HAVING
                quantidade > 1 
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Vinculo(s) empregaticio(s) repetido(s): '+ str(quantidade))

    return quantidade

#Verifica categoria eSocial nulo no motivo de rescisão
def eSocialNuloMotivoRescisao():

    resultado = select(
        """
            SELECT 
                i_motivos_resc,
                descricao,
                categoria_esocial
            FROM 
                bethadba.motivos_resc
            WHERE 
                categoria_esocial IS NULL
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('eSocial nulo no motivo de rescisão: '+ str(quantidade))

    return quantidade

#Verifica as folha que não foram fechadas confome competencia passada por parametro
def fechamentoFolha(competencia):

    resultado = select(
        """
            SELECT * FROM bethadba.processamentos WHERE i_competencias < {} AND pagto_realizado = 'N'
        """.format(competencia)
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Folhas que não foram fechadas até a competencia ' + str(competencia) + ': '+ str(quantidade))

    return quantidade

#Verifica as folhas de ferias sem data de pagamento
#A data de pagamento é obrigatória
def folhaFeriasDataPagamentoNulo():

    resultado = select(
        """
            SELECT 
                bethadba.dbf_getdatapagamentoferias(ferias.i_entidades,ferias.i_funcionarios,ferias.i_periodos,ferias.i_ferias) AS dataPagamento,
                i_entidades,
                i_ferias,
                i_funcionarios
            FROM 
                bethadba.ferias 
            WHERE 
                dataPagamento IS NULL;
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Folhas de ferias sem data de pagamento: '+ str(quantidade))

    return quantidade

#Verifica categoria eSocial nulo no motivo de aposentadoria
def eSocialNuloMotivoAposentadoria():

    resultado = select(
        """
            SELECT 
                i_motivos_apos,
                descricao,
                categoria_esocial
            FROM 
                bethadba.motivos_apos
            WHERE 
                categoria_esocial IS NULL
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('eSocial nulo no motivo de aposentadoria: '+ str(quantidade))

    return quantidade

#Verifica historicos salariais com salario zerado ou nulo

def historicoSalarialZerado():
    resultado = select(
        """
            SELECT * FROM bethadba.hist_salariais WHERE salario IN (0, NULL)
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Historico salarial com salario zerado: '+ str(quantidade))

    return quantidade

#Verifica data final maior que data de demissão

def dataFinalLancamentoMaiorDataRescisao():
    resultado = select(
        """
            SELECT 
                r.i_entidades, 
                r.i_funcionarios,
                DATEFORMAT(f.dt_admissao,'dd/MM/yyyy') AS dt_admissao,
                DATEFORMAT(f.dt_admissao,'01/MM/yyyy') AS dt_admissao_novo,
                DATEFORMAT(r.dt_rescisao,'dd/MM/yyyy') AS dt_resc,
                DATEFORMAT(r.dt_rescisao,'01/MM/yyyy') AS dt_resc_novo,
                DATEFORMAT(v.dt_inicial,'dd/MM/yyyy') AS ini_variavel,
                DATEFORMAT(v.dt_final,'dd/MM/yyyy') AS fim_variavel 
            FROM 
                bethadba.rescisoes r 
            INNER JOIN  
                bethadba.variaveis v ON (r.i_funcionarios = v.i_funcionarios AND r.i_entidades = v.i_entidades)
            INNER JOIN  
                bethadba.funcionarios f ON (r.i_funcionarios = f.i_funcionarios AND r.i_entidades = f.i_entidades)
            WHERE 
                v.dt_final > DATEFORMAT(r.dt_rescisao,'yyyy-MM-01') OR v.dt_inicial > DATEFORMAT(r.dt_rescisao,'yyyy-MM-01')
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Variaveis com data final maior que data de rescisão: '+ str(quantidade))

    return quantidade

#Busca as movimetação de pessoal repetidos
def movimentacaoPessoalRepetido():

    resultado = select(
        """
            SELECT 
                list(i_tipos_movpes), 
                descricao,
                count(descricao) AS quantidade 
            FROM 
                bethadba.tipos_movpes 
            GROUP BY 
                descricao 
            HAVING
                quantidade > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Movimetação de pessoal repetido(s): '+ str(quantidade))

    return quantidade

#Busca os tipos de afastamentos repetidos
def tipoAfastamentoRepetido():

    resultado = select(
        """
            SELECT 
                list(i_tipos_afast), 
                TRIM(descricao),
                count(descricao) AS quantidade 
            FROM 
                bethadba.tipos_afast 
            GROUP BY 
                TRIM(descricao) 
            HAVING
                quantidade > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Movimetação de pessoal repetido(s): '+ str(quantidade))

    return quantidade

#Busca as alterações de historicos dos funcionarios maior que a data de rescisão
def alteracaoFuncionarioMaiorDataRescisao():

    resultado = select(
        """
            SELECT
                hf.i_funcionarios,
                hf.i_entidades,
                hf.dt_alteracoes,
                r.dt_rescisao,
                STRING(r.dt_rescisao, ' ', SUBSTRING(hf.dt_alteracoes, 12, 8)) AS dt_alteracoes_novo
            FROM
                bethadba.hist_funcionarios hf
            INNER JOIN 
                bethadba.rescisoes r ON (hf.i_funcionarios = r.i_funcionarios AND hf.i_entidades = r.i_entidades)
            WHERE
                hf.dt_alteracoes > STRING(r.dt_rescisao, ' 23:59:59')
            ORDER BY 
            	hf.i_funcionarios, hf.dt_alteracoes DESC
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Data alteração de historico do funcionario maior que data de rescisão: '+ str(quantidade))

    return quantidade

#Busca as alterações de salario dos funcionarios maior que a data de rescisão
def alteracaoSalarialMaiorDataRescisao():

    resultado = select(
        """
            SELECT
                hs.i_funcionarios,
                hs.i_entidades,
                hs.dt_alteracoes,
                r.dt_rescisao,
                STRING(r.dt_rescisao, ' ', SUBSTRING(hs.dt_alteracoes, 12, 8)) AS dt_alteracoes_novo
            FROM
                bethadba.hist_salariais hs
            INNER JOIN 
                bethadba.rescisoes r ON (hs.i_funcionarios = r.i_funcionarios AND hs.i_entidades = r.i_entidades)
            WHERE
                hs.dt_alteracoes > STRING(r.dt_rescisao, ' 23:59:59')
            ORDER BY 
                hs.dt_alteracoes DESC
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Data alteração salarial do funcionario maior que data de rescisão: '+ str(quantidade))

    return quantidade

#Busca as alterações de cargo dos funcionarios maior que a data de rescisão
def alteracaoCargoMaiorDataRescisao():

    resultado = select(
        """
            SELECT
                hc.i_funcionarios,
                hc.i_entidades,
                hc.dt_alteracoes,
                r.dt_rescisao,
                STRING(r.dt_rescisao, ' ', SUBSTRING(hc.dt_alteracoes, 12, 8)) AS dt_alteracoes_novo
            FROM
                bethadba.hist_cargos hc
            INNER JOIN 
                bethadba.rescisoes r ON (hc.i_funcionarios = r.i_funcionarios AND hc.i_entidades = r.i_entidades)
            WHERE
                hc.dt_alteracoes > STRING(r.dt_rescisao, ' 23:59:59')
            ORDER BY 
                hc.dt_alteracoes DESC
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Data alteração de cargo do funcionario maior que data de rescisão: '+ str(quantidade))

    return quantidade

#Busca as classificações que estão com código errado no tipo de afastamento
def classificacaoErradaTipoAfastamento():

    resultado = select(
        """
            SELECT
                descricao
            FROM 
                bethadba.tipos_afast
            WHERE 
                classif IN (1, NULL)    
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Classificações que estão com código errado no tipo de afastamento: '+ str(quantidade))

    return quantidade

#Busca os tipos de atos repetidos
def tipoAtoRepetido():

    resultado = select(
        """
            SELECT 
                list(i_tipos_atos), 
                nome,
                count(nome) AS quantidade 
            FROM 
                bethadba.tipos_atos 
            GROUP BY 
                nome 
            HAVING
                quantidade > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Tipo de ato repetido(s): '+ str(quantidade))

    return quantidade

#Busca as descrições repetidas no horario ponto
def descricaoHorarioPontoRepetido():

    resultado = select(
        """
            SELECT 
                list(i_entidades), 
                list(i_horarios_ponto), 
                descricao,
                count(descricao) AS quantidade 
            FROM 
                bethadba.horarios_ponto 
            GROUP BY 
                descricao 
            HAVING
                quantidade > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Descricao do horario ponto repetido(s): '+ str(quantidade))

    return quantidade

#Busca as descrições repetidas na turma
def descricaoTurmaRepetido():

    resultado = select(
        """
            SELECT 
                list(i_entidades), 
                list(i_turmas), 
                descricao,
                count(descricao) AS quantidade 
            FROM 
                bethadba.turmas 
            GROUP BY 
                descricao 
            HAVING
                quantidade > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Descricao da turma repetido(s): '+ str(quantidade))

    return quantidade

#Buscar niveis de organogramas com separadores nulos
def nivelOrganogramaSeparadorNulo():

    resultado = select(
        """
            SELECT 
                * 
            FROM
                bethadba.niveis_organ 
            WHERE 
                separador_nivel IS NULL 
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Separadores nulos nos niveis de organogramas: '+ str(quantidade))

    return quantidade

#Verifica a natureza de texto juridico se é nulo nos atos
def atoNaturezaTextoJuridicoNulo():

    resultado = select(
        """
            SELECT 
                * 
            FROM 
                bethadba.atos 
            WHERE 
                i_natureza_texto_juridico IS NULL
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Natureza texto juridico do ato nulo: '+ str(quantidade))

    return quantidade

#Verifica se a data de fonte de divulgação é menor que a data de publicacao do ato
def atoFonteDivulgacaoMenorPublicacao():

    resultado = select(
        """
            SELECT 
                a.i_atos,
                fa.dt_publicacao,
                a.dt_publicacao	 
            FROM 
                bethadba.atos a
            INNER JOIN 
                bethadba.fontes_atos fa ON (fa.i_atos = a.i_atos)
            WHERE 
                fa.dt_publicacao < a.dt_publicacao
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Data de fonte de divulgação é menor que a data de publicacao do ato: '+ str(quantidade))

    return quantidade

#Ter ao menos um tipo de afastamento na configuração do cancelamento de férias
def tipoAfastamentoConfiguracaoCancelamentoFerias():

    resultado = select(
        """
            SELECT 
                *
            FROM 
                bethadba.canc_ferias cf
            WHERE 
                NOT EXISTS (SELECT i_tipos_afast FROM bethadba.canc_ferias_afast cfa WHERE cfa.i_canc_ferias = cf.i_canc_ferias)
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Tipo de afastamento na configuração do cancelamento de férias vazio: '+ str(quantidade))

    return quantidade

#Verifica descricao de cofiguração de organograma se é maior que 30 caracteres
def descricaoConfigOrganogramaMaior30():

    resultado = select(
        """
            SELECT 
                i_config_organ,
                descricao,
                LENGTH(descricao) AS tamanho 
            FROM 
                bethadba.config_organ
            WHERE 	
                tamanho > 30
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Descricao de cofiguração de organograma maior que 30 caracteres: '+ str(quantidade))

    return quantidade

#Verifica descricao de cofiguração de organograma repetido
def descricaoConfigOrganogramaRepetido():

    resultado = select(
        """
           SELECT 
                list(i_config_organ), 
                descricao, 
                count(descricao) AS quantidade 
            FROM 
                bethadba.config_organ 
            GROUP BY 
                descricao 
            HAVING 
                quantidade > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Descricao de cofiguração de organograma repetido(s): '+ str(quantidade))

    return quantidade

#Verifica se o CPF é invalido
def cpfInvalido():

    resultado = select(
        """
           SELECT
                i_pessoas,
                cpf
            FROM 
                bethadba.pessoas_fisicas
            WHERE
                cpf IS NOT NULL;
        """
    )

    quantidade = 0

    for i in resultado:
        cpf = i[1]
        
        if not validarCpf(cpf):
            quantidade += 1

    if quantidade == 0:
        return 0

    print('CPF invalido(s): '+ str(quantidade))

    return quantidade

#Verifica se o CNPJ é invalido
def cnpjInvalido():

    resultado = select(
        """
           SELECT
                i_pessoas,
                cnpj
            FROM 
                bethadba.pessoas_juridicas
        """
    )

    quantidade = 0

    for i in resultado:
        cnpj = i[1]
       
        if not validarCnpj(cnpj):
            quantidade += 1

    if quantidade == 0:
        return 0

    print('CNPJ invalido(s): '+ str(quantidade))

    return quantidade

#Verifica os RG's repetidos
def RgRepetido():

    resultado = select(
        """
            SELECT
                list(i_pessoas),
                rg,
                count(rg) AS quantidade
            FROM 
                bethadba.pessoas_fisicas 
            GROUP BY 
                rg 
            HAVING 
                quantidade > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('RG repetido(s): '+ str(quantidade))

    return quantidade

#Verifica os cargos com descricao repetidos
#Já existe um cargo com a descrição informada
def cargoDescricaoRepetido():

    resultado = select(
        """
            SELECT
                list(i_cargos),
                list(i_entidades),
                TRIM(nome),
                count(nome) AS quantidade
            FROM 
                bethadba.cargos 
            WHERE   
                i_entidades IN ({})
            GROUP BY 
                TRIM(nome) 
            HAVING 
                quantidade > 1
            ORDER BY
                quantidade
        """.format(idEntidadesAgrupadas)
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Cargo(s) repetido(s): '+ str(quantidade))

    return quantidade

#Verifica o termino de vigencia maior que 2099
#Essa verificação é necessaria para não dar loop ao migrar a pessoa fisica
def terminoVigenciaMaior2099():

    resultado = select(
        """
            SELECT 
                dt_vigencia_fin
            FROM 
                bethadba.bases_calc_outras_empresas
            WHERE 
                dt_vigencia_fin > 20990101
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Vigencia maior que 2099 em bases de calculos de outras empresas: '+ str(quantidade))

    return quantidade

#Verifica os emails invalidos
def emailInvalido():
    
    resultado = select(
        """
            SELECT 
                i_pessoas,
                email
            FROM 
                bethadba.pessoas
            WHERE 
                email IS NOT NULL
        """
    )

    quantidade = 0

    for i in resultado:
        idPessoa = i[0]
        email = i[1]

        if not validate_email(email) or len(email) < 5:
            quantidade += 1

    if quantidade == 0:
        return 0

    print('Email invalido: '+ str(quantidade))

    return quantidade

#Verifica o número de endereço se está vazio
def numeroEnderecoVazio():

    resultado = select(
        """
            SELECT 
                i_pessoas 
            FROM 
                bethadba.pessoas_enderecos 
            WHERE
                numero = ''
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Número de endereço vazio: '+ str(quantidade))

    return quantidade

#Verifica o nome de rua se está vazio
def nomeRuaVazio():

    resultado = select(
        """
            SELECT 
                * 
            FROM 
                bethadba.ruas 
            WHERE
                nome = '' OR
                nome IS NULL
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Nome da rua vazio: '+ str(quantidade))

    return quantidade

#Verifica os funcionarios sem previdencia
def funcionariosSemPrevidencia():

    resultado = select(
        """
            SELECT 
                hf.i_funcionarios,
                hf.i_entidades 
            FROM 
                bethadba.hist_funcionarios hf
            INNER JOIN 
                bethadba.funcionarios f ON (f.i_funcionarios = hf.i_funcionarios AND f.i_entidades = hf.i_entidades)
            WHERE
                hf.prev_federal = 'N' AND
                hf.prev_estadual = 'N' AND
                hf.fundo_ass = 'N' AND
                hf.fundo_prev = 'N' AND
                f.i_entidades IN ({}) AND
                f.tipo_func = 'F'
            GROUP BY
                hf.i_funcionarios,
                hf.i_entidades
            ORDER BY	
                hf.i_funcionarios
        """.format(idEntidadesAgrupadas)
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Funcionario sem previdencia: '+ str(quantidade))

    return quantidade

#Verifica os eventos de média/vantagem que não tem eventos vinculados
#Os eventos de composição da média são obrigatórios
def eventoMediaVantagemSemComposicao():

    resultado = select(
        """
            SELECT 
                DISTINCT(m.i_eventos),
                me.i_eventos_medias
            FROM 
                bethadba.mediasvant m
            LEFT JOIN
                mediasvant_eve me ON (m.i_eventos = me.i_eventos_medias)
            WHERE 
                me.i_eventos_medias IS NULL
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Eventos de média/vantagem compondo outros eventos: '+ str(quantidade))

    return quantidade

#Verifica os eventos de média/vantagem se estão compondo outros eventos de média/vantagem
#Eventos de composição não pode ser eventos de média/vantagem
def eventoMediaVantagemComposicao():

    resultado = select(
        """
            SELECT 
                i_eventos_medias,
                i_eventos
            FROM
                bethadba.mediasvant_eve 
            WHERE 
                i_eventos IN (SELECT i_eventos FROM bethadba.mediasvant)
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Eventos de média/vantagem sem composição de eventos: '+ str(quantidade))

    return quantidade

#Verifica a data de admissão da matrícula se é posterior a data de início da matrícula nesta lotação física
def dataAdmissaoMatriculaMaiorDataLotacaoFisica():

    resultado = select(
        """
           SELECT 
                f.dt_admissao,
                lm.i_funcionarios,
                lm.dt_inicial,
                lm.i_entidades,
                lm.i_locais_trab,
                lm.dt_final 
            FROM
                bethadba.funcionarios f
            INNER JOIN
                bethadba.locais_mov lm ON (f.i_funcionarios = lm.i_funcionarios AND f.i_entidades = lm.i_entidades)
            WHERE 
                f.dt_admissao > lm.dt_inicial 
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Data admissão matricula maior que data inicial de lotação fisica: '+ str(quantidade))

    return quantidade

#Verifica a descrição do motivo de alteração do ponto se contem mais que 30 caracteres
#A descrição não pode conter mais de 30 caracteres
def descricaoMotivoAlteracaoPontoMaior30():

    resultado = select(
        """
            SELECT
                i_motivos_altponto,
                LENGTH(descricao) AS tamanho_descricao
            FROM
                bethadba.motivos_altponto 
            WHERE 
                tamanho_descricao > 30 
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Descricao de motivos de alteração do ponto maior que 30 caracteres: '+ str(quantidade))

    return quantidade

#Verifica o motivo nos afastamentos se contem no máximo 150 caracteres
def observacaoAfastamentoMaior150():

    resultado = select(
        """
            SELECT 
                LENGTH(observacao) AS tamanho_observacao, 
                i_entidades, 
                i_funcionarios, 
                dt_afastamento 
            FROM
                bethadba.afastamentos 
            WHERE 
                LENGTH(observacao) > 150 
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Motivos nos afastamentos maior que 150 caracteres: '+ str(quantidade))

    return quantidade

#Verifica a data inicial no afastamento se é maior que a data final 
#A quantidade de dias não pode ser menor que 0
def dataInicialAfastamentoMaiorDataFinal():

    resultado = select(
        """
            SELECT 
                i_entidades, 
                i_funcionarios, 
                i_ferias,
                dt_gozo_ini,
                dt_gozo_fin 
            FROM 
                bethadba.ferias 
            WHERE 
                dt_gozo_ini > dt_gozo_fin
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Data inicial no afastamento é maior que a data final: '+ str(quantidade))

    return quantidade

#Busca as rescisões de aposentadoria com motivo nulo
#O motivo de rescisão é obrigatório
def motivoAposentadoriaNulo():

    resultado = select(
        """
            SELECT 
                i_entidades,
                i_funcionarios,
                i_rescisoes 
            FROM 
                bethadba.rescisoes 
            WHERE 
                i_motivos_resc = 7 AND 
                i_motivos_apos IS NULL
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Rescisões de aposentadoria com motivo nulo: '+ str(quantidade))

    return quantidade

#Verifica os grupos funcionais repetidos
def gruposFuncionaisRepetido():

    resultado = select(
        """
            SELECT
                list(i_entidades),
                list(i_grupos),
                nome,
                count(nome) AS quantidade
            FROM 
                bethadba.grupos
            WHERE
                i_entidades IN ({}) 
            GROUP BY 
                nome 
            HAVING 
                quantidade > 1
        """.format(idEntidadesAgrupadas)
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Grupos funcionais repetido(s): '+ str(quantidade))

    return quantidade

#Verifica a data inicial de beneficio do dependente se é melhor que a do titular
#A data inicial do benefício não pode ser menor que a data de admissão
#Plano de saude
def dataInicialDependenteMaiorTitular():

    resultado = select(
        """
            SELECT 
                fps.i_entidades,
                fps.i_funcionarios,
                fps.i_pessoas,
                fps.i_sequenciais,
                vigencia_inicial AS vigencia_inicial_dependente,
                vigencia_inicial_titular = (select vigencia_inicial FROM bethadba.func_planos_saude WHERE i_sequenciais = 1 AND i_funcionarios = fps.i_funcionarios)
            FROM 
                bethadba.func_planos_saude fps 
            WHERE 
                fps.i_sequenciais != 1 AND 
                fps.vigencia_inicial < vigencia_inicial_titular   
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('A data inicial do dependente maior do que do titular (Plano de Saude): '+ str(quantidade))

    return quantidade

#Verifica se o número de telefone na lotação fisica é maior que 11 caracteres
#O telefone pode conter no máximo 11 caracteres
def telefoneLotacaoFisicaMaior11():

    resultado = select(
        """
            SELECT 
                i_entidades,
                i_locais_trab,
                fone,
                LENGTH(fone) AS quantidade
            FROM 
                bethadba.locais_trab
            WHERE 
                quantidade > 11     
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Número de telefone na lotação fisica é maior que 11 caracteres: '+ str(quantidade))

    return quantidade

#Busca os atos com data inicial nulo
#A data de criação é obrigatória
def dataCriacaoAtoNulo():

    resultado = select(
        """
            SELECT 
                i_atos, 
                dt_vigorar 
            FROM
                bethadba.atos 
            WHERE
                dt_inicial IS NULL     
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Data de criação do ato é obrigatorio: '+ str(quantidade))

    return quantidade

#Busca as descrições repetidas dos niveis salariais
def descricaoNivelSalarialRepetido():

    resultado = select(
        """
            SELECT 
                list(i_entidades), 
                list(i_niveis), 
                TRIM(nome),
                count(nome) AS quantidade
            FROM 
                bethadba.niveis 
            GROUP BY 
                TRIM(nome)  
            HAVING
                quantidade > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Descricao de niveis salariais repetido(s): '+ str(quantidade))

    return quantidade

#Busca os cartões pontos que estão diferente de sua matricula ou repetidos
#Esta função só ira funcionar se os números das matriculas estiverem recodificados (que não se repetem)
def cartaoPontoRepetido():

    matriculas = select(
        """
            SELECT 
                list(i_entidades), 
                i_funcionarios, 
                count(*) AS quantidade 
            FROM 
                bethadba.funcionarios 
            WHERE
                i_entidades IN ({})    
            GROUP BY 
                i_funcionarios 
            HAVING 
                quantidade > 1 
            ORDER BY 
                i_funcionarios   
        """.format(idEntidadesAgrupadas)
    )

    if len(matriculas) > 0:
        return 0

    resultado = select(
        """
            SELECT 
                num_cp, 
                list(DISTINCT(i_funcionarios)), 
                COUNT(DISTINCT(i_funcionarios)) AS quantidade
            FROM 
                bethadba.hist_funcionarios 
            WHERE
                bate_cartao = 'S' AND num_cp IS NOT NULL
            GROUP BY 
                num_cp
            HAVING
                quantidade > 1
            ORDER BY 
                quantidade DESC
        """.format()
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Cartão ponto repetido(s): '+ str(quantidade))

    return quantidade

#Busca os funcionarios com data de nomeação maior que a data de posse
#O funcionário x da entidade x deve ter a data de posse (0000-00-00) posterior à data de nomeação (0000-00-00)!
def dataNomeacaoMaiorDataPosse():

    resultado = select(
        """
            SELECT 
                i_funcionarios 
            FROM 
                bethadba.hist_cargos
            WHERE
                dt_nomeacao > dt_posse
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Data de nomeação maior que data de posse: '+ str(quantidade))

    return quantidade

#Busca as contas bancarias dos funcionarios que estão invalidas
#Quando a forma de pagamento for "Crédito em conta" é necessário informar a conta bancária
def contaBancariaFuncionarioInvalida():

    resultado = select(
        """
            SELECT 
                f.i_funcionarios,
                f.i_entidades,
                hf.dt_alteracoes,
                hf.i_bancos AS banco_atual,
                hf.i_agencias AS agencia_atual,
                hf.i_pessoas_contas,
                pc.i_bancos AS banco_novo,
                pc.i_agencias AS agencia_nova
            FROM 
                bethadba.hist_funcionarios hf
            INNER JOIN 
                bethadba.funcionarios f ON (hf.i_funcionarios = f.i_funcionarios AND hf.i_entidades = f.i_entidades)
            INNER JOIN 
                bethadba.pessoas_contas pc ON (f.i_pessoas = pc.i_pessoas AND pc.i_pessoas_contas = hf.i_pessoas_contas)	
            WHERE 
                (pc.i_bancos != hf.i_bancos OR pc.i_agencias != hf.i_agencias) AND hf.forma_pagto = 'R'
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Historicos de funcionarios que estão com conta bancaria errada: '+ str(quantidade))

    return quantidade

#Busca os historicos de funcionarios com mais do que uma previdencia informada
#Apenas uma previdência pode ser informada
def previdenciaMaiorQueUm():

    resultado = select(
        """
            SELECT 
                i_funcionarios,
                i_entidades,
                dt_alteracoes,
                LENGTH(REPLACE(prev_federal || prev_estadual || fundo_ass || fundo_prev, 'N', '')) AS quantidade
            FROM 
                bethadba.hist_funcionarios
            WHERE
                quantidade > 1;
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Historicos de funcionarios com mais do que uma previdencia informada: '+ str(quantidade))

    return quantidade

#Busca os afastamentos com data inicial menor que data de admissão
#A data inicial não poderá ser menor que a data de admissão
def dataInicialAfastamentoMenorDataAdmissao():

    resultado = select(
        """
            SELECT 
                dt_afastamento, 
                dt_ultimo_dia, 
                i_entidades, 
                i_funcionarios, 
                (SELECT dt_admissao FROM bethadba.funcionarios WHERE i_funcionarios = a.i_funcionarios AND i_entidades = a.i_entidades) AS data_admissao 
            FROM 
                bethadba.afastamentos a
            WHERE 
                a.dt_afastamento < data_admissao;
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Afastamentos com data inicial menor que data de admissão: '+ str(quantidade))

    return quantidade

#Busca as areas de atuação com descrição repetido
#Já existe uma área de atuação com a descrição informada
def areasAtuacaoDescricaoRepetido():

    resultado = select(
        """
           SELECT 
                list(i_areas_atuacao), 
                TRIM(nome), 
                count(nome) 
            FROM 
                bethadba.areas_atuacao 
            GROUP BY 
                TRIM(nome) 
            HAVING 
                count(nome) > 1
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Áreas de atuação com descrição repetido: '+ str(quantidade))

    return quantidade

#Busca os dependentes sem motivo de termino
#O motivo de término é obrigatório
def dependenteMotivoTerminoNulo():

    resultado = select(
        """
            SELECT 
                i_pessoas ,
                i_dependentes,
                dt_ini_depende
            FROM 
                bethadba.dependentes d  
            WHERE 
                mot_fin_depende IS NULL AND 
                dt_fin_depende IS NOT NULL;
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Dependente sem motivo de termino: '+ str(quantidade))

    return quantidade

#Busca os cargos sem configuração de ferias
#A configuração de férias é obrigatória
def cargoConfiguracaoFeriasNulo():

    resultado = select(
        """
            SELECT 
                i_cargos, i_entidades 
            FROM 
                bethadba.cargos_compl
            WHERE
                i_config_ferias IS NULL OR 
                i_config_ferias_subst IS NULL
        """
    )

    quantidade = len(resultado)

    if quantidade == 0:
        return 0

    print('Cargos sem configuração de ferias: '+ str(quantidade))

    return quantidade

#-----------------------Executar---------------------#
pessoa_data_vencimento_cnh_menor_data_emissao()
pessoa_data_vencimento_cnh_menor_data_emissao()
pessoaDataVencimentoCNHMaiorNascimento()
campoAdicionalDescricaoRepetido()
dependentesOutros()
pessoaDataNascimentoNulo()
pessoaDataNascimentoMaiorDataDependecia()
pessoaDataNascimentoMaiorDataNascimentoResponsavel()
#cpfNulo()
cpfRepetido()
pisRepetido()
pisInvalido()
cnpjNulo()
logradourosDescricaoCaracterEspecial()
logradourosDescricaoRepetido()
tiposBasesRepetido()
logradourosSemCidade()
atosNumeroNulo()
atosRepetido()
cargoCboNulo()
eSocialNuloVinculoEmpregaticio()
vinculoEmpregaticioRepetido()
eSocialNuloMotivoRescisao()
fechamentoFolha(competenciaFechamentoFolha)
folhaFeriasDataPagamentoNulo()
eSocialNuloMotivoAposentadoria()
historicoSalarialZerado()
dataFinalLancamentoMaiorDataRescisao()
movimentacaoPessoalRepetido()
tipoAfastamentoRepetido()
alteracaoFuncionarioMaiorDataRescisao()
alteracaoSalarialMaiorDataRescisao()
alteracaoCargoMaiorDataRescisao()
classificacaoErradaTipoAfastamento()
tipoAtoRepetido()
descricaoHorarioPontoRepetido()
descricaoTurmaRepetido()
nivelOrganogramaSeparadorNulo()
atoNaturezaTextoJuridicoNulo()
atoFonteDivulgacaoMenorPublicacao()
tipoAfastamentoConfiguracaoCancelamentoFerias()
descricaoConfigOrganogramaMaior30()
descricaoConfigOrganogramaRepetido()
cpfInvalido()
cnpjInvalido()
RgRepetido()
cargoDescricaoRepetido()
terminoVigenciaMaior2099()
emailInvalido()
numeroEnderecoVazio()
nomeRuaVazio()
funcionariosSemPrevidencia()
eventoMediaVantagemSemComposicao()
eventoMediaVantagemComposicao()
dataAdmissaoMatriculaMaiorDataLotacaoFisica()
descricaoMotivoAlteracaoPontoMaior30()
observacaoAfastamentoMaior150()
dataInicialAfastamentoMaiorDataFinal()
motivoAposentadoriaNulo()
gruposFuncionaisRepetido()
dataInicialDependenteMaiorTitular()
telefoneLotacaoFisicaMaior11()
dataCriacaoAtoNulo()
descricaoNivelSalarialRepetido()
cartaoPontoRepetido()
dataNomeacaoMaiorDataPosse()
contaBancariaFuncionarioInvalida()
previdenciaMaiorQueUm()
dataInicialAfastamentoMenorDataAdmissao()
areasAtuacaoDescricaoRepetido()
dependenteMotivoTerminoNulo()
cargoConfiguracaoFeriasNulo()