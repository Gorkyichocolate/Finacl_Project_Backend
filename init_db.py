"""
Скрипт для инициализации базы данных
Создает тестовых пользователей
"""
import asyncio
import sys
import os

# Добавляем путь к backend в PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from configs.db import connect_to_mongodb, close_mongodb_connection
from repository.user import user_repository
from services.auth import get_password_hash


async def init_db():
    """Инициализация базы данных"""
    
    print("🔄 Подключение к MongoDB...")
    await connect_to_mongodb()
    
    print("\n📝 Создание тестовых пользователей...")
    
    # Тестовые пользователи
    test_users = [
        {
            "username": "johndoe",
            "email": "johndoe@example.com",
            "full_name": "John Doe",
            "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
            "disabled": False,
        },
        {
            "username": "alice",
            "email": "alicechains@example.com",
            "full_name": "Alice Chains",
            "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$g2/AV1zwopqUntPKJavBFw$BwpRGDCyUHLvHICnwijyX8ROGoiUPwNKZ7915MeYfCE",
            "disabled": True,
        },
        {
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "hashed_password": get_password_hash("test123"),
            "disabled": False,
        }
    ]
    
    for user_data in test_users:
        try:
            # Проверяем существование
            existing = await user_repository.get_user_by_username(user_data["username"])
            
            if existing:
                print(f"⚠️  Пользователь {user_data['username']} уже существует")
            else:
                await user_repository.create_user(user_data)
                print(f"✅ Создан пользователь: {user_data['username']}")
        except Exception as e:
            print(f"❌ Ошибка при создании {user_data['username']}: {e}")
    
    print("\n✅ Инициализация завершена!")
    print("\n📋 Тестовые учетные данные:")
    print("   Username: johndoe    | Password: secret")
    print("   Username: alice      | Password: secret2 (отключен)")
    print("   Username: testuser   | Password: test123")
    
    await close_mongodb_connection()


if __name__ == "__main__":
    asyncio.run(init_db())
