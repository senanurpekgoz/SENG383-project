"""
KidTask Uygulaması - Ana Program

Bu dosya, KidTask uygulamasının giriş noktasıdır.
"""

from kidtask_app import KidTaskApp
from user import User, UserRole
from task import Task
from wish import Wish
from datetime import datetime, timedelta


def main():
    """
    Ana program fonksiyonu.
    """
    print("=" * 50)
    print("KidTask Uygulamasına Hoş Geldiniz!")
    print("=" * 50)
    
    # Uygulama örneğini oluştur
    app = KidTaskApp(data_dir="data")
    
    # Verileri yükle
    print("\nVeriler yükleniyor...")
    app.load_data()
    
    # Örnek kullanıcılar oluştur (eğer yoksa)
    if len(app.users) == 0:
        print("\nÖrnek kullanıcılar oluşturuluyor...")
        
        child_user = User(
            username="ali",
            role=UserRole.CHILD,
            password="1234",
            total_points=0,
            level=1,
            ratings=[]
        )
        
        parent_user = User(
            username="anne",
            role=UserRole.PARENT,
            password="1234"
        )
        
        teacher_user = User(
            username="ogretmen",
            role=UserRole.TEACHER,
            password="1234"
        )
        
        app.users.extend([child_user, parent_user, teacher_user])
        print("Örnek kullanıcılar oluşturuldu.")
    
    # Örnek görev oluştur (eğer yoksa)
    if len(app.tasks) == 0:
        print("\nÖrnek görev oluşturuluyor...")
        example_task = Task(
            title="Odayı Temizle",
            description="Yatağını düzelt ve oyuncaklarını topla",
            due_date=datetime.now() + timedelta(days=1),
            points=20
        )
        app.tasks.append(example_task)
        print(f"Örnek görev oluşturuldu: {example_task.title}")
    
    # Örnek dilek oluştur (eğer yoksa)
    if len(app.wishes) == 0:
        print("\nÖrnek dilek oluşturuluyor...")
        example_wish = Wish(
            description="Yeni Oyuncak Araba",
            cost=100,
            required_level=1
        )
        app.wishes.append(example_wish)
        print(f"Örnek dilek oluşturuldu: {example_wish.description}")
    
    # Menü döngüsü
    while True:
        print("\n" + "=" * 50)
        print("MENÜ")
        print("=" * 50)
        print("1. Kullanıcıları Listele")
        print("2. Görevleri Listele")
        print("3. Dilekleri Listele")
        print("4. Görev Tamamla")
        print("5. Görev Onayla")
        print("6. Dilek Onayla")
        print("7. Verileri Kaydet")
        print("8. Çıkış")
        print("=" * 50)
        
        choice = input("\nSeçiminizi yapın (1-8): ").strip()
        
        if choice == "1":
            print("\n--- KULLANICILAR ---")
            for user in app.users:
                print(f"  {user}")
        
        elif choice == "2":
            print("\n--- GÖREVLER ---")
            for task in app.tasks:
                print(f"  {task}")
        
        elif choice == "3":
            print("\n--- DİLEKLER ---")
            for wish in app.wishes:
                print(f"  {wish}")
        
        elif choice == "4":
            if len(app.tasks) == 0:
                print("\nHenüz görev yok!")
                continue
            
            print("\n--- GÖREV TAMAMLA ---")
            for i, task in enumerate(app.tasks, 1):
                print(f"{i}. {task.title} - {'Tamamlandı' if task.is_completed else 'Devam Ediyor'}")
            
            try:
                task_num = int(input("\nTamamlanacak görev numarası: ")) - 1
                if 0 <= task_num < len(app.tasks):
                    app.tasks[task_num].complete()
                    print(f"✓ Görev tamamlandı: {app.tasks[task_num].title}")
                else:
                    print("Geçersiz görev numarası!")
            except ValueError:
                print("Lütfen geçerli bir sayı girin!")
        
        elif choice == "5":
            if len(app.tasks) == 0:
                print("\nHenüz görev yok!")
                continue
            
            print("\n--- GÖREV ONAYLA ---")
            completed_tasks = [t for t in app.tasks if t.is_completed and not t.is_approved]
            
            if not completed_tasks:
                print("Onay bekleyen tamamlanmış görev yok!")
                continue
            
            for i, task in enumerate(completed_tasks, 1):
                print(f"{i}. {task.title} (ID: {task.task_id})")
            
            try:
                task_num = int(input("\nOnaylanacak görev numarası: ")) - 1
                if 0 <= task_num < len(completed_tasks):
                    task = completed_tasks[task_num]
                    rating = float(input("Görev puanı (0-100): "))
                    child_username = input("Çocuk kullanıcı adı: ")
                    
                    approver_role = UserRole.PARENT  # Varsayılan olarak Parent
                    app.approve_task(task.task_id, rating, approver_role, child_username)
                    print("✓ Görev onaylandı!")
                else:
                    print("Geçersiz görev numarası!")
            except ValueError as e:
                print(f"Hata: {e}")
            except Exception as e:
                print(f"Beklenmeyen hata: {e}")
        
        elif choice == "6":
            if len(app.wishes) == 0:
                print("\nHenüz dilek yok!")
                continue
            
            print("\n--- DİLEK ONAYLA ---")
            pending_wishes = [w for w in app.wishes if not w.is_approved]
            
            if not pending_wishes:
                print("Onay bekleyen dilek yok!")
                continue
            
            for i, wish in enumerate(pending_wishes, 1):
                print(f"{i}. {wish.description} (ID: {wish.wish_id})")
            
            try:
                wish_num = int(input("\nOnaylanacak dilek numarası: ")) - 1
                if 0 <= wish_num < len(pending_wishes):
                    wish = pending_wishes[wish_num]
                    approver_role = UserRole.PARENT  # Varsayılan olarak Parent
                    app.approve_wish(wish.wish_id, approver_role)
                    print("✓ Dilek onaylandı!")
                else:
                    print("Geçersiz dilek numarası!")
            except ValueError as e:
                print(f"Hata: {e}")
            except Exception as e:
                print(f"Beklenmeyen hata: {e}")
        
        elif choice == "7":
            try:
                app.save_data()
                print("✓ Veriler başarıyla kaydedildi!")
            except Exception as e:
                print(f"Hata: {e}")
        
        elif choice == "8":
            print("\nVeriler kaydediliyor...")
            try:
                app.save_data()
                print("✓ Veriler kaydedildi. Çıkılıyor...")
            except Exception as e:
                print(f"Kaydetme hatası: {e}")
            print("\nGüle güle!")
            break
        
        else:
            print("\nGeçersiz seçim! Lütfen 1-8 arası bir sayı girin.")


if __name__ == "__main__":
    main()

