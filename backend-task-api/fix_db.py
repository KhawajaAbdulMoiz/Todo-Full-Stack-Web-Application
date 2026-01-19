import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

# Get your Neon PostgreSQL URL
DATABASE_URL = os.getenv('DATABASE_URL')
print(f'Connecting to: {DATABASE_URL[:50]}...')

async def fix_database():
    try:
        # Connect to PostgreSQL
        conn = await asyncpg.connect(DATABASE_URL)
        print('✓ Connected to database')
        
        # 1. Check what tables exist
        tables = await conn.fetch('''
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        ''')
        print('\nTables in database:')
        for table in tables:
            print(f'  - {table["table_name"]}')
        
        # 2. Check user tables
        print('\nChecking user tables:')
        
        # Check 'user' table
        try:
            user_count = await conn.fetchval('SELECT COUNT(*) FROM "user"')
            print(f'  "user" table: {user_count} rows')
        except:
            print('  "user" table: does not exist')
        
        # Check 'users' table  
        try:
            users_count = await conn.fetchval('SELECT COUNT(*) FROM users')
            print(f'  users table: {users_count} rows')
            
            # Show some users
            if users_count > 0:
                users = await conn.fetch('SELECT id, email FROM users LIMIT 3')
                print('  Sample users:')
                for user in users:
                    print(f'    {user["id"]}: {user["email"]}')
        except:
            print('  users table: does not exist')
        
        # 3. Check task table foreign keys
        print('\nChecking task table foreign keys:')
        try:
            constraints = await conn.fetch('''
                SELECT conname, conrelid::regclass, confrelid::regclass 
                FROM pg_constraint 
                WHERE conrelid = 'task'::regclass
            ''')
            for con in constraints:
                print(f'  Constraint: {con["conname"]}')
                print(f'    Table: {con["conrelid"]}')
                print(f'    References: {con["confrelid"]}')
        except:
            print('  No task table or constraints found')
        
        # 4. Fix the foreign key automatically
        print('\n=== FIXING FOREIGN KEY ===')
        
        # Drop wrong foreign key
        await conn.execute('ALTER TABLE task DROP CONSTRAINT IF EXISTS task_user_id_fkey;')
        print('✓ Dropped wrong foreign key')
        
        # Add correct foreign key
        await conn.execute('''
            ALTER TABLE task 
            ADD CONSTRAINT task_user_id_fkey 
            FOREIGN KEY (user_id) REFERENCES users(id);
        ''')
        print('✓ Added correct foreign key to users table')
        
        # Drop empty 'user' table if exists
        try:
            await conn.execute('DROP TABLE IF EXISTS "user" CASCADE;')
            print('✓ Removed duplicate user table')
        except:
            print('✓ No duplicate user table to remove')
        
        print('\n✓ Fix completed! Restart your backend.')
        
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if 'conn' in locals():
            await conn.close()
            print('Connection closed')

asyncio.run(fix_database())