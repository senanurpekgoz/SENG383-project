"""
Setup script to create initial users and sample data for KidTask application.
"""

from kidtask_app import KidTaskApp
from user import User, UserRole
from task import Task
from wish import Wish
from datetime import datetime, timedelta


def setup_initial_data():
    """Create initial users and sample data."""
    app = KidTaskApp()
    
    # Create sample users
    child1 = User(
        username="ali",
        role=UserRole.CHILD,
        password="1234",
        total_points=0,
        level=1,
        ratings=[]
    )
    
    child2 = User(
        username="ayse",
        role=UserRole.CHILD,
        password="1234",
        total_points=0,
        level=1,
        ratings=[]
    )
    
    parent1 = User(
        username="parent1",
        role=UserRole.PARENT,
        password="1234"
    )
    
    teacher1 = User(
        username="teacher1",
        role=UserRole.TEACHER,
        password="1234"
    )
    
    app.users = [child1, child2, parent1, teacher1]
    
    # Create sample tasks
    task1 = Task(
        title="Odanı Temizle",
        description="Yatağını yap, oyuncaklarını topla",
        due_date=datetime.now() + timedelta(days=1),
        points=20,
        child_username="ali",
        created_by="parent1"
    )
    
    task2 = Task(
        title="Matematik Ödevi",
        description="Sayfa 45-50 arası problemleri çöz",
        due_date=datetime.now() + timedelta(days=2),
        points=30,
        child_username="ayse",
        created_by="teacher1"
    )
    
    app.tasks = [task1, task2]
    
    # Create sample wishes
    wish1 = Wish(
        description="Yeni oyuncak araba",
        cost=100,
        required_level=1,
        child_username="ali",
        wish_type="product"
    )
    
    wish2 = Wish(
        description="Sinemaya gitmek",
        cost=150,
        required_level=2,
        child_username="ayse",
        wish_type="activity"
    )
    
    app.wishes = [wish1, wish2]
    
    # Save data
    app.save_data()
    print("Örnek veriler oluşturuldu!")
    print(f"Kullanıcılar: {len(app.users)}")
    print(f"Görevler: {len(app.tasks)}")
    print(f"Dilekler: {len(app.wishes)}")
    print("\nÖrnek giriş bilgileri:")
    print("Çocuk: ali / 1234")
    print("Çocuk: ayse / 1234")
    print("Ebeveyn: parent1 / 1234")
    print("Öğretmen: teacher1 / 1234")


if __name__ == "__main__":
    setup_initial_data()

