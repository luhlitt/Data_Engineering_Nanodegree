import configparser
import psycopg2

immigration = """
    SELECT count(*) FROM immigration
"""

port_locations = """
    SELECT count(*) FROM port_locations
"""

airport_code = """
    SELECT count(*) FROM airport_code
"""

temperature = """
    SELECT count(*) FROM temperature
"""

demographics = """
    SELECT count(*) FROM demographics
"""
    
def check_count(cur, conn, table_name):
    """
    Checks whether there are no empty tables.
    """
    for query in table_name:
        cur.execute(query)
        conn.commit()
        if cur.rowcount < 1:
            print("No data found in table: {} ".format(query))


def main():
    config = configparser.ConfigParser()
    config.read('dl.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    table_name = [immigration, port_locations, airport_code, temperature, demographics]

    check_count(cur, conn, table_name)

    conn.close()


if __name__ == "__main__":
    main()