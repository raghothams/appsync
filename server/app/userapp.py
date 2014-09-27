
import psycopg2
import psycopg2.extras
import conf
import json
import traceback


class UserApp:


    def __init__(self):

        # Connect to db
        self.db = psycopg2.connect(
                                    database=conf.PG_DB,
                                    host=conf.PG_HOST,
                                    port=conf.PG_PORT,
                                    user=conf.PG_USER,
                                    password=conf.PG_PASSWORD
                                  )

    def set(self, user_id, apps):

        result = None
        cur = self.db.cursor()

        try:

            query = "UPDATE public.users SET apps = %s WHERE id = %s"
            cur.execute(query, (psycopg2.extras.Json(apps), user_id))

            if cur.rowcount == 1: 

                self.db.commit()
                result = True

        except psycopg2.DatabaseError as e:
            cur.close()
            raise e
            #print traceback.format_exc(e)
                
        cur.close()
        return result



    def get(self, user_id):

        result = None
        cur = self.db.cursor()

        try:

            query = "SELECT apps from public.users WHERE id = %s"
            cur.execute(query, (user_id,))

            row = cur.fetchone()
            return row[0]

        except Exception as e:
            cur.close()
            print traceback.format_exc(e)
            raise e

                
        cur.close()
        return result

