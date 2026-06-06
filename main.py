import asyncio
from orm import AsyncORM

async def main():
    await AsyncORM.create_tables()
    await AsyncORM.add_user_with_sub("Slava", "Standard", 30)
    await AsyncORM.add_user_with_sub("Pavel", "Go", 30)
    await AsyncORM.add_user_with_sub("Andrey", "Start", 30)
    await AsyncORM.add_user_with_sub("Alexey", "Pro", 30)
    await AsyncORM.get_all_users_with_their_subs()

asyncio.run(main())