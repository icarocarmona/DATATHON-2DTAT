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
select  t."IdAluno", t."IdUnidade", t."Sexo" , t."EstadoCivil" , t."DataNascimento" , t."CorRaca" , t."EnsinoMedio_IdEstabelecimentoEnsino" , 
t."EnsinoMedio_AnoConclusao" , t2."IdTurma" , t2."IdSituacaoAlunoTurma" , t2."DataSituacaoAtivo" , t2."DataSituacaoInativo" , t2."DataHoraEfetivacaoMatricula", 
t2."ProblemaAutorizadoMatricula" , t2."IdMotivoInativacao" , t2."ComentarioInativacao" , t2."IdPlanoPagamento_Matricula" , t3."MotivoInativacao" 
from magic_steps.tbaluno t 
FULL OUTER JOIN magic_steps.tbalunoturma t2 on t."IdAluno" = t2."IdAluno" 
FULL OUTER JOIN magic_steps.tbmotivoinativacao t3 on t2."IdMotivoInativacao" = t3."IdMotivoInativacao" ;


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
