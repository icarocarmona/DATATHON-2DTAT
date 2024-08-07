-- A tabela merged_data_aluno na coluna IdMotivoInativacao estava vindo com varchar, mas o campo da tabela de relação tbmotivoinativacao é int
-- Por isso ajustamos os valores 
 
select * from magic_steps.tbmotivoinativacao t limit 10

select distinct "IdMotivoInativacao" from magic_steps.merged_data_aluno mda

select * from magic_steps.merged_data_aluno
WHERE "IdMotivoInativacao" = '11.0';

UPDATE magic_steps.merged_data_aluno
set "IdMotivoInativacao" =
case 
	when "IdMotivoInativacao" = '2.0' then '2'
	when "IdMotivoInativacao" = '11.0' then '11'
	when "IdMotivoInativacao" = '9.0' then '9'
	else "IdMotivoInativacao"
end;

-- Descobri que a MergeAluno não estão com todos os dados, por isso criei uma view mais completa, mais focada para ver a questão da inativação, 
-- mas pode ser melhorada adicionando as novas colunas

create or replace view vw_aluno  as
select  t."IdAluno",t."IdUnidade", t."Sexo" , t."EstadoCivil" , t."DataNascimento" , t."CorRaca" , t."EnsinoMedio_IdEstabelecimentoEnsino" , 
t."EnsinoMedio_AnoConclusao" , t2."IdTurma" , t2."IdSituacaoAlunoTurma" , t2."DataSituacaoAtivo" , t2."DataSituacaoInativo" , t2."DataHoraEfetivacaoMatricula", 
t2."ProblemaAutorizadoMatricula" , t2."IdMotivoInativacao" , t2."ComentarioInativacao" , t2."IdPlanoPagamento_Matricula" , t3."MotivoInativacao", tm."SituacaoAlunoTurma" ,
extract(year  from age(current_date, t."DataNascimento"::timestamp )) as idade,
obs."DataOcorrencia", obs."ObservacaoRegistro", tip."IdTipoOcorrencia", tip."NomeTipoOcorrencia"
from magic_steps.tbaluno t 
join magic_steps.tbalunoobs obs on t."IdAluno" = obs."IdAluno" 
join magic_steps.tbtipoocorrencia tip on tip."IdTipoOcorrencia" = obs."IdTipoOcorrencia" 
JOIN magic_steps.tbalunoturma t2 on t."IdAluno" = t2."IdAluno" 
FULL OUTER JOIN magic_steps.tbmotivoinativacao t3 on t2."IdMotivoInativacao" = t3."IdMotivoInativacao" 
join magic_steps.tbsituacaoalunoturma_m tm on t2."IdSituacaoAlunoTurma" = tm."IdSituacaoAlunoTurma" 
;



select * from magic_steps.tbalunoobs t limit 100;

create or replace view magic_steps.vw_aluno_inativo as
select va.*, obs."DataOcorrencia", obs."DataInclusao", obs."ObservacaoLiberacao", oc."NomeTipoOcorrencia", oc."IdTipoOcorrencia" from vw_aluno va 
left join magic_steps.tbalunoobs obs on va."IdAluno" = obs."IdAluno" 
left join magic_steps.tbtipoocorrencia oc  on obs."IdTipoOcorrencia" = oc."IdTipoOcorrencia" 
where va."IdMotivoInativacao" is not null;


select  * from tbtipoocorrencia t ;
--31	Psicol da família: Atividade Passos em família

select * from magic_steps.vw_aluno_inativo limit 100;


select distinct "NomeTipoOcorrencia" from magic_steps.vw_aluno_inativo limit 100;

select * from magic_steps.vw_aluno_inativo 
where "IdTipoOcorrencia" = 31
limit 100;


---

select count(distinct "IdAluno" ) from vw_aluno va where "IdMotivoInativacao" is null;

select count(distinct "IdAluno" ) from vw_aluno_inativo vai; 


-----


CREATE OR REPLACE VIEW magic_steps.vw_aluno_obs
AS SELECT va."IdAluno",
    va."IdUnidade",
    va."Sexo",
    va."EstadoCivil",
    va."DataNascimento",
    va."CorRaca",
    va."EnsinoMedio_IdEstabelecimentoEnsino",
    va."EnsinoMedio_AnoConclusao",
    va."IdTurma",
    va."IdSituacaoAlunoTurma",
    va."DataSituacaoAtivo",
    va."DataSituacaoInativo",
    va."DataHoraEfetivacaoMatricula",
    va."ProblemaAutorizadoMatricula",
    va."IdMotivoInativacao",
    va."ComentarioInativacao",
    va."IdPlanoPagamento_Matricula",
    va."MotivoInativacao",
    obs."DataOcorrencia",
    obs."DataInclusao",
    obs."ObservacaoLiberacao",
    oc."NomeTipoOcorrencia"
   FROM vw_aluno va
     LEFT JOIN magic_steps.tbalunoobs obs ON va."IdAluno" = obs."IdAluno"
     LEFT JOIN magic_steps.tbtipoocorrencia oc ON obs."IdTipoOcorrencia" = oc."IdTipoOcorrencia"
  WHERE va."IdMotivoInativacao" IS NOT NULL;



  ---





-- ENTENDENDO COMO FUNCIONA A NOTA POR DISCIPLINA
select d.*, t.*from tbfasenotaaluno t 
join tbdisciplina d on d."IdDisciplina" = t."IdDisciplina"  
and t."IdAluno" ='199'

-- CRIANDO ALUNO RESUMIDO PARA FACILITAR
create table tb_aluno_resumido as 
select "IdAluno", "IdUnidade", "Sexo", "DataNascimento", "CorRaca" from tbaluno t 

--- CRIANDO ALUNO TURMA RESUMIDO
create table magic_steps.tb_aluno_turma_resumida as 
select   "IdTurma", "IdAluno","IdSituacaoAlunoTurma", "DataSituacaoAtivo", "DataSituacaoInativo", "DataHoraEfetivacaoMatricula", "IdMotivoInativacao", 
"ComentarioInativacao" , "Comentario" , "IdAlunoCurso" , "IdAlunoTurma" 
from  tbalunoturma t ;


-- FILTREI UM ALUNO QUALQUER PARA TESTAR
select * from tb_aluno_resumido t
where t."IdAluno" = '199';

--- ENTENDENDO COMO FUNCIONANA A SITUACAO DO ALUNO POR TURMA
select * from tbalunoturma t 
join tbsituacaoalunoturma_m tm on tm."IdSituacaoAlunoTurma"  = t."IdSituacaoAlunoTurma"
where t."IdAluno" = '199'
and t."DataSituacaoAtivo" between '2023-01-01 00:00:00' and '2023-12-30 00:00:00'
;

--- ENTENDENDO A NOTA DO ALUNO E DISCIPLINA COM TESTE DO ALUNO
select d.*, t.*from tbfasenotaaluno t 
join tbdisciplina d on d."IdDisciplina" = t."IdDisciplina"  
and t."IdAluno" ='199'

-- CRIANDO UMA TABELA COMPLETA COM A NOTA DO ALUNO POR DISCIPLINA E TURMA
create table tb_aluno_full as
SELECT 
t1."IdAluno" AS "t1_IdAluno", t1."IdFaseNotaAtual" AS "t1_IdFaseNotaAtual", t1."IdTurma" AS "t1_IdTurma", t1."IdUsuarioMatricula" AS "t1_IdUsuarioMatricula", t1."IdSituacaoAlunoDisciplina" AS "t1_IdSituacaoAlunoDisciplina", t1."StGoogleEdu_Sincronizado" AS "t1_StGoogleEdu_Sincronizado", t1."IdDisciplina" AS "t1_IdDisciplina", t1."IdMotivoTrancamento" AS "t1_IdMotivoTrancamento", t1."ComentarioTrancamento" AS "t1_ComentarioTrancamento", t1."NotaFinal" AS "t1_NotaFinal", t1."Faltas" AS "t1_Faltas", t1."ProblemaAutorizadoMatricula" AS "t1_ProblemaAutorizadoMatricula", t1."IdUsuarioAutorizacaoMatricula" AS "t1_IdUsuarioAutorizacaoMatricula", t1."JustificativaAutorizacaoMatricula" AS "t1_JustificativaAutorizacaoMatricula", t1."GoogleForEducation_LogProcessamento" AS "t1_GoogleForEducation_LogProcessamento", t1."SituacaoAtual" AS "t1_SituacaoAtual", t1."StDisciplinaDispensada" AS "t1_StDisciplinaDispensada", t1."IdAlunoCurso" AS "t1_IdAlunoCurso", t1."DataMatricula" AS "t1_DataMatricula", t1."DataTrancamento" AS "t1_DataTrancamento", t1."IdUsuarioTrancamento" AS "t1_IdUsuarioTrancamento", t2."BaseComum" AS "t2_BaseComum", t2."UsoEscola" AS "t2_UsoEscola", t2."TipoDisciplina" AS "t2_TipoDisciplina", t2."CargaHorariaEstagio" AS "t2_CargaHorariaEstagio", t2."QtdeAulas" AS "t2_QtdeAulas", t2."CodigoAgrupamento" AS "t2_CodigoAgrupamento", t2."ES_CargaHoraria" AS "t2_ES_CargaHoraria", t2."Educacenso_CodigoDisciplina" AS "t2_Educacenso_CodigoDisciplina", t2."NumeroOrdemHistorico" AS "t2_NumeroOrdemHistorico", t2."ES_ConteudoProgramatico" AS "t2_ES_ConteudoProgramatico", t2."CargaHorariaTotal" AS "t2_CargaHorariaTotal", t2."CargaHorariaPratica" AS "t2_CargaHorariaPratica", t2."CargaHorariaTeorica" AS "t2_CargaHorariaTeorica", t2."QtdeCreditos" AS "t2_QtdeCreditos", t2."Ementa" AS "t2_Ementa", t2."ObjGeral" AS "t2_ObjGeral", t2."ObjEspecificos" AS "t2_ObjEspecificos", t2."Bibliografia" AS "t2_Bibliografia", t2."BibliografiaComplementar" AS "t2_BibliografiaComplementar", t2."Metodologia" AS "t2_Metodologia", t2."Recursos" AS "t2_Recursos", t2."FormaDeAvaliacao" AS "t2_FormaDeAvaliacao", t2."ConteudoProgramatico" AS "t2_ConteudoProgramatico", t2."NomeDisciplina" AS "t2_NomeDisciplina", t2."SiglaDisciplina" AS "t2_SiglaDisciplina", t2."Competencias" AS "t2_Competencias", t2."AulasPraticas" AS "t2_AulasPraticas", t2."TIAcodigo" AS "t2_TIAcodigo", t3."IdSituacaoAlunoTurma" AS "t3_IdSituacaoAlunoTurma", t3."IdMotivoInativacao" AS "t3_IdMotivoInativacao", t3."IdAlunoTurma" AS "t3_IdAlunoTurma", t3."DataHoraEfetivacaoMatricula" AS "t3_DataHoraEfetivacaoMatricula", t3."ComentarioInativacao" AS "t3_ComentarioInativacao", t3."Comentario" AS "t3_Comentario", t3."DataSituacaoAtivo" AS "t3_DataSituacaoAtivo", t3."DataSituacaoInativo" AS "t3_DataSituacaoInativo", t4."IdFaseNota" AS "t4_IdFaseNota", t4."Nota01" AS "t4_Nota01", t4."Nota02" AS "t4_Nota02", t4."IdFormulaComposicao" AS "t4_IdFormulaComposicao", t4."StNotaConfirmada" AS "t4_StNotaConfirmada", t4."NotaFase" AS "t4_NotaFase", t4."QuantAulasDadas" AS "t4_QuantAulasDadas", t4."StNotaFaseExibirDisp" AS "t4_StNotaFaseExibirDisp", t4."IdFaseNotaAluno" AS "t4_IdFaseNotaAluno", t4."Nota10" AS "t4_Nota10", t4."_Nota01" AS "t4__Nota01", t4."Nota03" AS "t4_Nota03", t4."Nota04" AS "t4_Nota04", t4."Nota05" AS "t4_Nota05", t4."Nota06" AS "t4_Nota06", t4."Nota07" AS "t4_Nota07", t4."Nota08" AS "t4_Nota08", t4."Nota09" AS "t4_Nota09", t5."StPermitirDigitacaoNotaFalta" AS "t5_StPermitirDigitacaoNotaFalta", t5."StPermiteAssinaturaEletronica" AS "t5_StPermiteAssinaturaEletronica", t5."CdSituacaoEducaCenso" AS "t5_CdSituacaoEducaCenso", t5."DominioSituacaoAlunoTurma" AS "t5_DominioSituacaoAlunoTurma", t5."SituacaoAlunoTurma" AS "t5_SituacaoAlunoTurma", t5."SituacaoSistema" AS "t5_SituacaoSistema", t5."SituacaoAcademica" AS "t5_SituacaoAcademica", t6."StDispensarNotaAutomatica" AS "t6_StDispensarNotaAutomatica", t6."IdPeriodo" AS "t6_IdPeriodo", t6."IdSerie" AS "t6_IdSerie", t6."NumeroFase" AS "t6_NumeroFase", t6."IdFaseNotaAprovacao" AS "t6_IdFaseNotaAprovacao", t6."IdFaseNotaReprovacao" AS "t6_IdFaseNotaReprovacao", t6."NumeroOrdemExibicao" AS "t6_NumeroOrdemExibicao", t6."StCalcularSituacaoGeral" AS "t6_StCalcularSituacaoGeral", t6."IdFormulaAprovacaoFrequencia" AS "t6_IdFormulaAprovacaoFrequencia", t6."ValorNotaMaxima" AS "t6_ValorNotaMaxima", t6."StCalcDiscCompUtilizaFormulaFN" AS "t6_StCalcDiscCompUtilizaFormulaFN", t6."StConfirmarDispensaAutomatica" AS "t6_StConfirmarDispensaAutomatica", t6."StFaseNotaSempreCalcular" AS "t6_StFaseNotaSempreCalcular", t6."StPermiteProfessorImportarPadraoAvaliacao" AS "t6_StPermiteProfessorImportarPadraoAvaliacao", t6."StPermiteProfessorInserirEditarAvaliacao" AS "t6_StPermiteProfessorInserirEditarAvaliacao", t6."StPermiteProfessorInserirBloco" AS "t6_StPermiteProfessorInserirBloco", t6."ImprimirBoletimNotaParcial" AS "t6_ImprimirBoletimNotaParcial", t6."ImprimirBoletimNPNaoConfirmada" AS "t6_ImprimirBoletimNPNaoConfirmada", t6."ImprimirBoletimNota" AS "t6_ImprimirBoletimNota", t6."ImprimirBoletimFaltas" AS "t6_ImprimirBoletimFaltas", t6."StFaseInformada" AS "t6_StFaseInformada", t6."StCalcularDisciplinaComposta" AS "t6_StCalcularDisciplinaComposta", t6."IdFormulaComposicaoNota" AS "t6_IdFormulaComposicaoNota", t6."IdFormulaNota" AS "t6_IdFormulaNota", t6."MediaMinimaAprovacao" AS "t6_MediaMinimaAprovacao", t6."ValorArredondamentoMedia" AS "t6_ValorArredondamentoMedia", t6."IdFormulaAprovacao" AS "t6_IdFormulaAprovacao", t6."IdFormulaFalta" AS "t6_IdFormulaFalta", t6."NomeFase" AS "t6_NomeFase", t6."CabecBoletim" AS "t6_CabecBoletim", t6."SituacaoAprovado" AS "t6_SituacaoAprovado", t6."DataLimiteDigitacaoNota" AS "t6_DataLimiteDigitacaoNota", t6."NumeroDiasLetivos" AS "t6_NumeroDiasLetivos", t6."DataInicioExibicao" AS "t6_DataInicioExibicao", t6."SituacaoReprovado" AS "t6_SituacaoReprovado", t6."NumeroSemanasLetivas" AS "t6_NumeroSemanasLetivas", t6."TipoDispensaAutomatica" AS "t6_TipoDispensaAutomatica", t6."TipoInformada" AS "t6_TipoInformada", t6."SituacaoReprovadoFrequencia" AS "t6_SituacaoReprovadoFrequencia", t6."DataInicialPeriodoAula" AS "t6_DataInicialPeriodoAula", t6."DataFinalPeriodoAula" AS "t6_DataFinalPeriodoAula", t7."IdUnidade" AS "t7_IdUnidade", t7."Sexo" AS "t7_Sexo", t7."DataNascimento" AS "t7_DataNascimento", t7."CorRaca" AS "t7_CorRaca", extract(year from age(current_date, t7."DataNascimento"::timestamp)) as idade
FROM tbsituacaoalunodisciplina t1
JOIN tbdisciplina t2 ON t2."IdDisciplina" = t1."IdDisciplina"
JOIN tb_aluno_turma_resumida t3 ON t3."IdTurma" = t1."IdTurma" AND t3."IdAluno" = t1."IdAluno"
JOIN tbfasenotaaluno t4 ON t4."IdDisciplina" = t2."IdDisciplina" AND t3."IdTurma" = t4."IdTurma" AND t4."IdAluno" = t3."IdAluno"
JOIN tbsituacaoalunoturma_m t5 ON t5."IdSituacaoAlunoTurma" = t3."IdSituacaoAlunoTurma"
JOIN tbfasenota t6 ON t6."IdFaseNota" = t4."IdFaseNota"
JOIN tb_aluno_resumido t7 ON t7."IdAluno" = t3."IdAluno";


drop  table tb_aluno_full;


select * from tb_aluno_full t 
where t."t1_IdAluno" = '199'
and t."t3_DataSituacaoAtivo" between '2022-01-01 00:00:00' and '2022-12-30 00:00:00'



----
--- NOTA FASE MEDIA DAS NOTAS (t4_NotaFase)
select t2."MotivoInativacao" , t."t2_NomeDisciplina" ,t.idade,t."t7_CorRaca", t."t7_Sexo", t."t3_DataSituacaoAtivo",
t."t3_DataSituacaoInativo" ,"t3_DataHoraEfetivacaoMatricula" , extract(days from (t."t3_DataSituacaoInativo"::timestamp - t."t3_DataHoraEfetivacaoMatricula"::timestamp)) as dias_matriculado
, t.* from tb_aluno_full t 
join tbmotivoinativacao t2 on t."t3_IdMotivoInativacao" = t2."IdMotivoInativacao" 
where "t3_IdMotivoInativacao" is not null 
and "t1_IdAluno" = '578'
and t."t3_DataHoraEfetivacaoMatricula" between '2022-01-01 00:00:00' and '2022-12-30 00:00:00'
