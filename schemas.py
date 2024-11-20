import graphene
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    with psycopg2.connect(DATABASE_URL) as conn:
        print("success database connection")
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            print("Query executed successfully")
except psycopg2.Error as e:
    print(f"Database error: {e}")


class Position(graphene.ObjectType):
    id = graphene.Int()
    description = graphene.String()


class Professional(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    position = graphene.Field(Position)
    position_id = graphene.Int()

    def resolve_position(self, info):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, description FROM djangoapp_position WHERE id = %s",
                    (self.position_id,)
                )

                position_data = cur.fetchone()
                if position_data:
                    return Position(id=position_data[0], description=position_data[1])

class Query(graphene.ObjectType):
    allProfessionals = graphene.List(Professional)
    professional_by_id = graphene.Field(Professional, id=graphene.Int(required=True))
    allPositions = graphene.List(Position)
    position_by_id = graphene.Field(Position, id=graphene.Int(required=True))
    professionals_by_name = graphene.List(Professional, name=graphene.String(required=True))

    def resolve_allProfessionals(self, info):
        try:
            print("here")
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    query = "SELECT id, name, position_id FROM djangoapp_professional"
                    print(query)
                    cur.execute(query)
                    professionals = []
                    for data in cur.fetchall():
                        professionals.append(Professional(id=data[0], name=data[1], position_id=data[2]))
                    return professionals 
        except psycopg2.Error as e:
            print(f"Database error: {e}")

    def resolve_professional_by_id(self, info, id):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name, position_id FROM djangoapp_professional WHERE id = %s",
                    (id,)
                )

                data = cur.fetchone()

                if data:
                    return Professional(id=data[0], name=data[1], position_id=data[2])

    def resolve_allPositions(self, info):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, description FROM djangoapp_position")
                return [Position(id=data[0], description=data[1]) for data in cur.fetchall()]


    def resolve_position_by_id(self, info, id):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, description FROM djangoapp_position WHERE id = %s", (id,))
                data = cur.fetchone()

                if data:
                    return Position(id=data[0], description=data[1])

    def resolve_professionals_by_name(self, info, name):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name, position_id FROM djangoapp_professional WHERE name LIKE %s",
                    (f'%{name}%',)
                )

                return [
                    Professional(id=data[0], name=data[1], position_id=data[2])
                    for data in cur.fetchall()
                ]

def get_schema():
    return graphene.Schema(query=Query)