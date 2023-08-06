import requests
import time
from abc import ABC, abstractmethod
import json
from datetime import datetime, timedelta
from typing import Union
import typer
import click


class ReExecution(ABC):
    def __init__(self, id_arquivos: list, sleep_time: int = 30, user: str = "ReExecution"):
        self.user = user
        self.sleep_time = sleep_time
        self.id_arquivos = id_arquivos
        self.set_id_arquivos = set(self.id_arquivos)
        self._parser_request()

    @property
    @abstractmethod
    def get_etl_step(self) -> str:
        pass

    @property
    @abstractmethod
    def get_name_ids(self) -> str:
        pass

    @staticmethod
    def countdown(t: int):
        typer.echo("\n")
        while t >= 0:
            typer.echo(f'Aguardando {t} segundos para enviar o proximo lote.    \r', nl=False)
            time.sleep(1)
            t -= 1
        typer.echo('                                                    \r', nl=False)

    def _parser_request(self):
        # Measure time to finish:
        total_seconds = len(self.set_id_arquivos) * self.sleep_time
        m, s = divmod(total_seconds, 60)
        h, m = divmod(m, 60)

        currently_time = datetime.now()
        time_add = timedelta(hours=h, minutes=m, seconds=s)
        typer.echo(f"\n<> Há {len(self.set_id_arquivos)} {self.get_name_ids}")
        typer.echo(f"<> Previsão de hora: {(currently_time + time_add).strftime('%H:%M:%S')}")

        h, m, s = list(
            map(
                lambda x: f"0{x}" if len(str(x)) == 1 else x, [h, m, s]
            )
        )

        typer.echo(f"<> Tempo estimado: {h}h {m}min {s}s\n")

    def run(self, prioritario: bool = True, printar_ids: bool = False):
        if self.sleep_time == 0:
            self._send_request(prioritario=prioritario)
            c = 1
            enviados = list(self.set_id_arquivos)
        else:
            c = 0
            enviados = []
            with typer.progressbar(enumerate(self.set_id_arquivos), len(self.set_id_arquivos)) as progress:
                for idx, id_ in progress:
                    try:
                        self._send_request(id_, prioritario=prioritario)

                        if printar_ids:
                            typer.echo(f"  id atual: {id_}")
                        c += 1
                        enviados.append(id_)

                        self.countdown(self.sleep_time)
                    except KeyboardInterrupt:
                        typer.echo(typer.style("\n\nExecução pausada!\n", fg=typer.colors.YELLOW))
                        typer.echo(f"<> Ainda faltam {len(self.set_id_arquivos) - c} ids para enviar\n")
                        option = typer.prompt(
                            "Deseja (C)ontinuar, (A)lterar o intervalo entre requisições ou (P)arar (entre a letra correspondente à opção desejada)?",
                            type=click.Choice(["c", "a", "p", "continuar", "alterar", "parar"], case_sensitive=False),
                            show_choices=False
                        )
                        if option[:1] == 'a':
                            self.sleep_time = typer.prompt("Entre o novo tempo de execução", type=click.IntRange(0))

                            # Remeasuring time to finish:
                            total_seconds = (len(self.set_id_arquivos) - len(enviados)) * self.sleep_time
                            m, s = divmod(total_seconds, 60)
                            h, m = divmod(m, 60)

                            currently_time = datetime.now()
                            time_add = timedelta(hours=h, minutes=m, seconds=s)
                            typer.echo(f"\n<> Há {len(self.set_id_arquivos) - c} {self.get_name_ids} ids restantes")
                            typer.echo(f"<> Nova previsão de término: {(currently_time + time_add).strftime('%H:%M:%S')}")
                        elif option[:1] == 'p':
                            typer.echo(
                                "\n" + typer.style('Execução interrompida pelo usuário.                    ',
                                typer.colors.RED)
                            )
                            return
                    except Exception as e:
                        typer.echo("\n" + typer.style("ERRO!", fg=typer.colors.BRIGHT_RED))
                        typer.echo(f'\nFoi encontrada a seguinte exceção ao reprocessar o id "{id_}": {e}')
                        if not typer.confirm("Deseja tentar novamente", prompt_suffix="? "):
                            raise e
                        while True:
                            try:
                                self._send_request(id_, prioritario=prioritario)
                                break
                            except Exception as e:
                                typer.echo("\n" + typer.style("ERRO!", fg=typer.colors.BRIGHT_RED))
                                typer.echo(f'\nFoi encontrada a seguinte exceção ao reprocessar o id "{id_}": {e}')
                                if not typer.confirm("Deseja tentar novamente", prompt_suffix="? "):
                                    raise e
        typer.echo(typer.style("\nSUCESSO\n", fg=typer.colors.GREEN, bold=True))
        typer.echo(f"{c} mensagens enviadas")
        typer.echo(f"ids enviados: {enviados}")

    def _send_request(self, id: Union[int, None] = None, prioritario: bool = False):
        url = 'https://v8wcnj1p11.execute-api.us-east-1.amazonaws.com/Prod/'
        headers = {
            "x-api-key": "GfkRdSHPM5rNBHgX2b4FVzuqDma7jhTT5utt7mY9kQ735pWekGp8jV6AayRSYF8q",
            "Content-Type": "application/json"
        }

        body = {
            "endpoint": "icdb-prod",
            "input-type": "multiple-id",
            "input": [id] if id is not None else list(self.set_id_arquivos),
            "etl-step": self.get_etl_step,
            "usuario": f"ReExecution - {self.user}"
        }
        if prioritario:
            body["prioridade"] = "true"

        body = json.dumps(body)

        response = requests.post(url, data=body, headers=headers)
        if not response.ok:
            raise ConnectionError(f"Erro ao processar a requisição de reprocessamento ({response.status_code}): {response.content}")

class ReProcessar(ReExecution):
    def __init__(self, id_arquivos: list, sleep_time: int = 30, user: str = "ReExecution"):
        super().__init__(id_arquivos, sleep_time, user)

    @property
    def get_etl_step(self) -> str:
        return "posprocessamento"

    @property
    def get_name_ids(self) -> str:
        return "id_arquivos"


class ReLoad(ReExecution):
    def __init__(self, id_arquivos: list, sleep_time: int = 30, user: str = "ReExecution"):
        super().__init__(id_arquivos, sleep_time, user)

    @property
    def get_etl_step(self) -> str:
        return "load"

    @property
    def get_name_ids(self) -> str:
        return "id_arquivo_padronizados"


class RePadronizar(ReExecution):
    def __init__(self, id_arquivos: list, sleep_time: int = 30, user: str = "ReExecution"):
        super().__init__(id_arquivos, sleep_time, user)

    @property
    def get_etl_step(self) -> str:
        return "padronizacao"

    @property
    def get_name_ids(self) -> str:
        return "id_arquivo_parseados"


class ReParsear(ReExecution):
    def __init__(self, id_arquivos: list, sleep_time: int = 30, user: str = "ReExecution"):
        super().__init__(id_arquivos, sleep_time, user)

    @property
    def get_etl_step(self) -> str:
        return "parser"

    @property
    def get_name_ids(self) -> str:
        return "id_arquivo_originais"
