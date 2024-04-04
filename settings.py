from dotenv import dotenv_values

####################################################################
#                            DATABASE                              #
####################################################################
DB = dotenv_values('.env.postgres')
# DB = dotenv_values('.env.postgres.local')
sqlalchemy_url = (f'postgresql+asyncpg://{DB["POSTGRES_USER"]}:'
                  f'{DB["POSTGRES_PASSWORD"]}@{DB["POSTGRES_HOST"]}:'
                  f'{DB["POSTGRES_PORT"]}/{DB["POSTGRES_DB"]}')