from ic_toolkit_edd.abstract.utilities import read_credentials
import pandas as pd
import pymysql

credentials = read_credentials()


def executa_query(query):
    try:
        connection = pymysql.connect(user=credentials['userDB'],
                                     password=credentials['passwordDB'],
                                     host=credentials['hostDB'],
                                     port=int(credentials['portDB']),
                                     db=credentials['nameDB'],
                                     connect_timeout=5,
                                     cursorclass=pymysql.cursors.DictCursor,
                                     local_infile=True)
    except Exception as e:
        print(f'Erro ao criar conexao {e}')

    with connection.cursor() as cur:
        cur.execute(query)
        df_results = pd.DataFrame(cur.fetchall())
    connection.close()
    return df_results
