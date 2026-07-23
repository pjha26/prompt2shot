import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect('postgresql://postgres.lhxjmwpgimdfrfeejijn:cG2%26HM3eB4%24PZHF@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres')
    print('Connected!')
    await conn.close()

asyncio.run(test())
