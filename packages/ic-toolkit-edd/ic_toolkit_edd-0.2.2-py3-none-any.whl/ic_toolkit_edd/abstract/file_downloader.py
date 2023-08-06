import os
import boto3
import botocore
import typer
from .database import executa_query
from .utilities import FileIdTypes


def download_file(file_type: FileIdTypes, id_type: FileIdTypes, id_arquivo: str,  path: str) -> None:
    id_field = "id_arquivo" + (f"_{id_type.value}" if id_type != FileIdTypes.arquivo else "")
    query = f"select * from upload.pipeline where {id_field} in ({id_arquivo})"
    result = executa_query(query)
    target_id_field = f"id_arquivo_{file_type.value}"
    unique_ids = result[id_field].unique()
    unique_target_ids = result[result[id_field].isin(unique_ids)][target_id_field].unique()
    target_bucket = file_type.value[:4] + '_s3_bucket'
    target_prefix = file_type.value[:4] + '_caminho_s3'
    target_filename = file_type.value[:4] + '_nome_arquivo'
    with typer.progressbar(range(len(unique_target_ids)), length=len(unique_ids)) as progress:
        for i in progress:
            try:
                result_line = result[result[target_id_field] == unique_target_ids[i]].iloc[0]
                prefix = result_line[target_prefix]
                file_name = result_line[target_filename]
                bucket = result_line[target_bucket]
                key = prefix + file_name
                s3 = boto3.resource('s3')
            except Exception as e:
                typer.echo(" " + typer.style("ERRO AO DETERMINAR A LOCALIZAÇÃO DOS ARQUIVOS!"))
                typer.echo(f"\nA seguinte exceção foi encontrada: {e}")
            try:
                s3.Bucket(bucket).download_file(key, os.path.join(path, file_name))
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    typer.echo(" " + typer.style("ARQUIVO INEXISTENTE NA S3", fg=typer.colors.WHITE, bg=typer.colors.RED))
                    return
                else:
                    typer.echo(" " + typer.style("ERRO AO BAIXAR O(S) ARQUIVO(S) NA S3", fg=typer.colors.WHITE, bg=typer.colors.RED))
                    typer.echo(f"\n{e}\n")
                    return
        typer.echo(typer.style(" SUCESSO", fg=typer.colors.GREEN, bold=True))
        typer.echo(f"\n{len(unique_target_ids)} arquivos baixados!")
