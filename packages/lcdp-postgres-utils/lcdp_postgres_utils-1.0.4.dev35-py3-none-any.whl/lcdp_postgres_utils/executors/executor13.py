from ..utils import get_connection


# Executor for postgres 13
class Executor13:
    dbz_publication_name = "dbz_publication"
    dbz_signal_tablename = "debezium_signal"

    def __init__(self, database_name,  endpoint, user_name, db_password, decrypt_func):
        self.database_name = database_name
        self.__connection = get_connection(database_name, endpoint, user_name, db_password, decrypt_func)
        self.cursor = self.__connection.cursor()
        self.logs = []

    def get_logs(self):
        return self.logs

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.__connection:
            self.__connection.close()

    # ~~~~~ SQL String ~~~~~ #
    def __create_database_sql(self, database_name):
        return "CREATE DATABASE \"{0}\" ENCODING UTF8;".format(database_name)

    def __create_debezium_signal_table_sql(self, cdc_user_name):
        return """
      CREATE TABLE \"{0}\" (
        id   varchar(42) CONSTRAINT debezium_signal_pk PRIMARY KEY,
        type varchar(32) NOT NULL,
        data varchar(2048)
      );
      GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON \"{1}\" TO \"{2}\";
    """.format(Executor13.dbz_signal_tablename,
               Executor13.dbz_signal_tablename,
               cdc_user_name)

    def __create_immutable_unaccent_function(self):
        return """
      CREATE OR REPLACE FUNCTION immutable_unaccent(text)
        RETURNS text AS
      $func$
        SELECT unaccent('unaccent', $1)
      $func$  LANGUAGE sql IMMUTABLE PARALLEL SAFE STRICT;
    """

    def __create_immutable_array_to_text_function(self):
        return """
      CREATE OR REPLACE FUNCTION immutable_array_to_searchable_text(text[])
      returns text as
      $func$
          select array_to_string($1, '~^~')
      $func$ LANGUAGE sql IMMUTABLE PARALLEL SAFE STRICT;
    """

    def __create_french_with_stop_word_dictionary(self):
        return """
      DO
        $$BEGIN
        CREATE TEXT SEARCH CONFIGURATION french_with_stop_word ( COPY = pg_catalog.french );
        CREATE TEXT SEARCH DICTIONARY french_with_stop_word_dict (
            Template = snowball
            , Language = french
            );
        EXCEPTION
          when unique_violation then null;
        END;$$;
      ALTER TEXT SEARCH CONFIGURATION french_with_stop_word ALTER MAPPING FOR  asciiword, asciihword, hword_asciipart, hword, hword_part, word WITH french_with_stop_word_dict;
    """

    def __create_nextval_basedontime(self):
        return """
      CREATE OR REPLACE FUNCTION nextval_basedontime(sequence_regclass regclass, date_format text)
          RETURNS bigint AS
          $func$
      DECLARE
          next_val bigint;
          base_time bigint;
          curr_val bigint;
      BEGIN
          -- lock the function to avoid to set a wrong value to reference_sequence
          PERFORM pg_advisory_lock(sequence_regclass::bigint);

          -- get current time and compare with reference_sequence
          base_time := to_char(now(), date_format)::bigint;
          EXECUTE format('SELECT last_value FROM %I', sequence_regclass) INTO curr_val;

          IF (curr_val < base_time)
          THEN
              PERFORM setval(sequence_regclass, base_time);
          END IF;

          next_val = nextval(sequence_regclass);

          -- unlock
          PERFORM pg_advisory_unlock(sequence_regclass::bigint);

          RETURN next_val;
      END
      $func$ LANGUAGE plpgsql PARALLEL SAFE;
    """

    def __create_unaccent_extension(self):
        return "CREATE EXTENSION IF NOT EXISTS unaccent;"

    def __create_pg_trgm_extension(self):
        return "CREATE EXTENSION IF NOT EXISTS pg_trgm;"

    def __create_publication(self, value):
        return "CREATE PUBLICATION \"{0}\" FOR ALL TABLES;".format(value)

    def __create_schema(self, schema_name):
        return "CREATE SCHEMA IF NOT EXISTS \"{0}\";".format(schema_name)

    def __create_user_sql(self, user_name, user_password):
        return "CREATE USER \"{0}\" WITH PASSWORD '{1}';".format(user_name, user_password)

    def __alter_database_owner_sql(self, database_name, user_name):
        return "ALTER DATABASE \"{0}\" OWNER TO \"{1}\";".format(database_name, user_name)

    def __alter_database_work_mem_sql(self, value):
        return "ALTER DATABASE \"{0}\" SET work_mem TO \"{1}\";".format(self.database_name, value)

    def __grant_schema_read_only_user_sql(self, user_name, schema_name):
        return """
    GRANT CONNECT ON DATABASE \"{2}\" TO \"{1}\";
    GRANT USAGE ON SCHEMA \"{0}\" TO \"{1}\";
    GRANT SELECT ON ALL TABLES IN SCHEMA  \"{0}\" TO \"{1}\";
    GRANT SELECT ON ALL SEQUENCES IN SCHEMA  \"{0}\" TO \"{1}\";
    ALTER DEFAULT PRIVILEGES IN SCHEMA \"{0}\" GRANT SELECT ON TABLES TO \"{1}\";
    ALTER DEFAULT PRIVILEGES IN SCHEMA \"{0}\" GRANT SELECT ON SEQUENCES TO \"{1}\";
    """.format(schema_name, user_name, self.database_name)

    def __grant_create_table(self, user_name):
        return f"GRANT CREATE, TEMPORARY ON DATABASE \"{self.database_name}\" TO \"{user_name}\";"

    def __grant_replication_user_sql(self, user_name):
        return "GRANT rds_replication TO \"{0}\";".format(user_name)

    def __grant_superuser_user_sql(self, user_name):
        return "GRANT rds_superuser TO \"{0}\";".format(user_name)

    def __grant_schema_all_access(self, user_name, schema_name):
        return """
    GRANT CONNECT ON DATABASE \"{2}\" TO \"{1}\";
    GRANT USAGE ON SCHEMA \"{0}\" TO \"{1}\";
    GRANT ALL ON ALL TABLES IN SCHEMA \"{0}\" TO \"{1}\";
    GRANT ALL ON ALL SEQUENCES IN SCHEMA  \"{0}\" TO \"{1}\";
    ALTER DEFAULT PRIVILEGES IN SCHEMA \"{0}\" GRANT ALL ON TABLES TO \"{1}\";
    ALTER DEFAULT PRIVILEGES IN SCHEMA \"{0}\" GRANT ALL ON SEQUENCES TO \"{1}\";
    """.format(schema_name, user_name, self.database_name)

    def __check_user_sql(self, user_name):
        return "select * from pg_user where usename = '{0}';".format(user_name)

    def __check_database_sql(self, database_name):
        return "select * from pg_database where datname = '{0}';".format(database_name)

    def __check_table_sql(self, value):
        return "select * from pg_tables where tablename = '{0}';".format(value)

    def __check_debezium_signal_table_sql(self):
        return self.__check_table_sql(Executor13.dbz_signal_tablename)

    def __check_database_unaccent_extension(self):
        return "select * from pg_extension where extname = 'unaccent';"

    def __check_database_pg_trgm_extension(self):
        return "select * from pg_extension where extname = 'pg_trgm';"

    def __check_publication_sql(self, value):
        return "select * from pg_publication where pubname = '{0}';".format(value)

    # ~~~~~ Log action ~~~~~ #
    def __log_create_user(self, user_name):
        return "Creation de l'utilisateur : {0} \n".format(user_name)

    def __log_create_database(self, database_name):
        return "Creation de la base de donnees : {0} \n".format(database_name)

    def __log_create_debezium_signal_table(self):
        return "Creation de la table {0} pour la base de donnees : {1} \n".format(Executor13.dbz_signal_tablename, self.database_name)

    def __log_create_unaccent_extension(self):
        return "Creation de l'extension unaccent pour la base de donnees : {0} \n".format(self.database_name)

    def __log_create_unaccent_immutable_function(self):
        return "Creation la fonction immutable de l'extension unaccent pour la base de donnees : {0} \n".format(self.database_name)

    def __log_create_immutable_array_to_text_function_function(self):
        return "Creation la fonction immutable de transformation de tableau en texte cherchable pour la base de donnees : {0} \n".format(self.database_name)

    def __log_create_french_with_stop_word_dictionary(self):
        return "Creation du dictionnaire français avec les mots de liaison inclu pour la base de donnees : {0} \n".format(self.database_name)

    def __log_create_nextval_basedontime(self):
        return "Creation de la fonction permettant d'obtenir une valeur de séquence aligné sur le temps : {0} \n".format(self.database_name)

    def __log_create_pg_trgm_extension(self):
        return "Creation de l'extension pg_trgm pour la base de donnees : {0} \n".format(self.database_name)

    def __log_create_publication(self, value):
        return "Creation de la publication {0} pour la base de donnees : {1} \n".format(value, self.database_name)

    def __log_alter_database_work_mem(self):
        return "Modification de la valeur work_mem pour la base de donnees : {0} \n".format(self.database_name)

    def __log_alter_database_owner(self, database_name, user_name):
        return "L'utilisateur {0} est proprietaire de la base {1} \n" \
            .format(user_name, database_name)

    def __log_grant_schema_read_only_user(self, user_name, schema_name):
        return "L'utilisateur {0} a herite des droits read only sur le schema {1} \n".format(user_name, schema_name)

    def __log_grant_create_table(self, user_name):
        return "L'utilisateur {0} a herite des droits de creation de base de table sur la base de données {1} \n"\
            .format(user_name, self.database_name)

    def __log_grant_replication_user(self, user_name):
        return "L'utilisateur {0} a herite des droits replication \n".format(user_name)

    def __log_grant_superuser_user(self, user_name):
        return "L'utilisateur {0} a herite des droits superuser \n".format(user_name)

    def __log_create_schema(self, schema_name):
        return "Creation du schema {0} si il n'existe pas \n".format(schema_name)

    def __log_grant_schema_all_access(self, user_name, schema_name):
        return "L'utilisateur {0} a herite de tous les droits sur le schema {1} \n".format(user_name, schema_name)

    # ~~~~~ Execute action in DB ~~~~~ #
    def __execute_select_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def __execute_create_user(self, user_name, user_password):
        if not self.__execute_select_query(self.__check_user_sql(user_name)):
            self.cursor.execute(self.__create_user_sql(user_name, user_password))
            return self.__log_create_user(user_name)

    def __execute_create_database(self, database_name):
        if not self.__execute_select_query(self.__check_database_sql(database_name)):
            self.cursor.execute(self.__create_database_sql(database_name))
            return self.__log_create_database(database_name)

    def __execute_create_unaccent_extension(self):
        if not self.__execute_select_query(self.__check_database_unaccent_extension()):
            self.cursor.execute(self.__create_unaccent_extension())
            return self.__log_create_unaccent_extension()

    def __execute_create_immutable_unaccent_function(self):
        self.cursor.execute(self.__create_immutable_unaccent_function())
        return self.__log_create_unaccent_immutable_function()

    def __execute_create_immutable_array_to_text_function(self):
        self.cursor.execute(self.__create_immutable_array_to_text_function())
        return self.__log_create_immutable_array_to_text_function_function()

    def __execute_create_french_with_stop_word_dictionary(self):
        self.cursor.execute(self.__create_french_with_stop_word_dictionary())
        return self.__log_create_french_with_stop_word_dictionary()

    def __execute_create_nextval_basedontime(self):
        self.cursor.execute(self.__create_nextval_basedontime())
        return self.__log_create_nextval_basedontime()

    def __execute_create_pg_trgm_extension(self):
        if not self.__execute_select_query(self.__check_database_pg_trgm_extension()):
            self.cursor.execute(self.__create_pg_trgm_extension())
            return self.__log_create_pg_trgm_extension()

    def __execute_create_publication(self, value):
        if not self.__execute_select_query(self.__check_publication_sql(value)):
            self.cursor.execute(self.__create_publication(value))
            return self.__log_create_publication(value)

    def __execute_create_debezium_signal_table(self, cdc_user_name):
        if not self.__execute_select_query(self.__check_debezium_signal_table_sql()):
            self.cursor.execute(self.__create_debezium_signal_table_sql(cdc_user_name))
            return self.__log_create_debezium_signal_table()

    def __alter_database_owner(self, database_name, user_name):
        self.cursor.execute(self.__alter_database_owner_sql(database_name, user_name))
        return self.__log_alter_database_owner(database_name, user_name)

    def __alter_database_work_mem(self, value):
        self.cursor.execute(self.__alter_database_work_mem_sql(value))
        return self.__log_alter_database_work_mem()

    def __execute_grant_schema_read_only(self, user_name, schema_name):
        self.cursor.execute(self.__grant_schema_read_only_user_sql(user_name, schema_name))
        return self.__log_grant_schema_read_only_user(user_name, schema_name)

    def __execute_grant_create_table(self, user_name):
        self.cursor.execute(self.__grant_create_table(user_name))
        return self.__log_grant_create_table(user_name)

    def __execute_grant_replication(self, user_name):
        self.cursor.execute(self.__grant_replication_user_sql(user_name))
        return self.__log_grant_replication_user(user_name)

    def __execute_grant_superuser(self, user_name):
        self.cursor.execute(self.__grant_superuser_user_sql(user_name))
        return self.__log_grant_superuser_user(user_name)

    def __execute_create_schema(self, schema_name):
        self.cursor.execute(self.__create_schema(schema_name))
        return self.__log_create_schema(schema_name)

    def __execute_grant_schema_all_access(self, user_name, schema_name):
        self.cursor.execute(self.__grant_schema_all_access(user_name, schema_name))
        return self.__log_grant_schema_all_access(user_name, schema_name)

    # ~~~~~ Execute multiple action in DB ~~~~~ #
    def create_service(self, database_name, user_name, user_password):
        log_user = self.__execute_create_user(user_name, user_password)
        log_database = self.__execute_create_database(database_name)
        log_alter = self.__alter_database_owner(database_name, user_name)
        self.logs.extend(list(filter(None, [log_user, log_database, log_alter])))

    def create_unaccent_extension(self):
        log_unaccent_extension = self.__execute_create_unaccent_extension()
        self.logs.extend(list(filter(None, [log_unaccent_extension])))

    def create_unaccent_immutable_function(self):
        log = self.__execute_create_immutable_unaccent_function()
        self.logs.extend(list(filter(None, [log])))

    def create_immutable_array_to_text_function(self):
        log = self.__execute_create_immutable_array_to_text_function()
        self.logs.extend(list(filter(None, [log])))

    def execute_create_french_with_stop_word_dictionary(self):
        log = self.__execute_create_french_with_stop_word_dictionary()
        self.logs.extend(list(filter(None, [log])))

    def execute_create_nextval_basedontime(self):
        log = self.__execute_create_nextval_basedontime()
        self.logs.extend(list(filter(None, [log])))

    def create_pg_trgm_extension(self):
        log_pg_trgm_extension = self.__execute_create_pg_trgm_extension()
        self.logs.extend(list(filter(None, [log_pg_trgm_extension])))

    def create_user(self, user_name, user_password):
        log_user = self.__execute_create_user(user_name, user_password)
        self.logs.extend(list(filter(None, [log_user])))

    def create_cdc_user(self, user_name, user_password):
        log_user = self.__execute_create_user(user_name, user_password)
        log_grant_replication = self.__execute_grant_replication(user_name)
        self.logs.extend(list(filter(None, [log_user, log_grant_replication])))

    def create_schema(self, schema_name):
        log_create_schema = self.__execute_create_schema(schema_name)
        self.logs.extend(list(filter(None, [log_create_schema])))

    def set_work_mem(self, value):
        log_work_mem = self.__alter_database_work_mem(value)
        self.logs.extend(list(filter(None, [log_work_mem])))

    def setup_hawking(self, hawking_user_name):
        log_grant_read_only = self.__execute_grant_schema_read_only(hawking_user_name, "public")
        self.logs.extend(list(filter(None, [log_grant_read_only])))

    def setup_cdc(self, cdc_user_name):
        log_grant_read_only = self.__execute_grant_schema_read_only(cdc_user_name, "public")
        log_publication = self.__execute_create_publication(Executor13.dbz_publication_name)
        log_debezium_signal_table = self.__execute_create_debezium_signal_table(cdc_user_name)
        self.logs.extend(list(filter(None, [log_grant_read_only, log_publication, log_debezium_signal_table])))

    def setup_schema_write_user(self, user_name, schema_name):
        log_grant_access = self.__execute_grant_schema_all_access(user_name, schema_name)
        self.logs.extend(list(filter(None, [log_grant_access])))

    def setup_schema_read_only_user(self, user_name, schema_name):
        log_grant_access = self.__execute_grant_schema_read_only(user_name, schema_name)
        self.logs.extend(list(filter(None, [log_grant_access])))

    def setup_etl_user(self, user_name):
        log_grant_create_table = self.__execute_grant_create_table(user_name)
        self.logs.extend(list(filter(None, [log_grant_create_table])))
