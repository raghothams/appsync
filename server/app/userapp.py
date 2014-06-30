
import psycopg2
import psycopg2.extras
import conf
import datetime
import uuid


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

    def init(self, user_id):

        result = None
        cur = self.db.cursor()

        try:

            apps = []
            query = "INSERT into public.user_apps (user_id, apps) VALUES (%s, %s) RETURNING user_id"
            cur.execute(query, (user_id, apps ))

            if cur.rowcount == 1: 

                self.db.commit()
                result = True
                print "done init for new user"

        except Exception as e:
            print e
                
        finally:
            cur.close()
            return result


    def update(self, user_id, apps):

        result = None
        cur = self.db.cursor()

        try:

            print apps
            print user_id
            query = "UPDATE public.user_apps SET apps = %s WHERE user_id = %s"
            cur.execute(query, (apps, user_id, ))

            if cur.rowcount == 1: 

                self.db.commit()
                result = True

        except Exception as e:
            print e
            #print traceback.format_exc(e)
                
        finally:
            cur.close()
            return result



    def get(self, user_id):

        result = None
        cur = self.db.cursor()

        try:

            query = "SELECT * from public.user_apps WHERE user_id = %s"
            cur.execute(query, (user_id,))

            row = cur.fetchone()
            print row

            result = {}
            result['last_updated'] = row[2]
            result['apps'] = row[1]
            result['user'] = row[0]

        except Exception as e:
            print traceback.format_exc(e)
                
        finally:
            cur.close()
            return result

