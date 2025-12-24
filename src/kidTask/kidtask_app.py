"""
KidTaskApp - KidTask uygulamasının ana yönetici sınıfı.

Bu sınıf, tüm görevleri, dilekleri ve kullanıcıları yönetir,
verileri dosyaya kaydeder ve yükler.
"""

import json
import os
from typing import Optional, List
from datetime import datetime

from task import Task
from wish import Wish
from user import User, UserRole


class KidTaskApp:
    """
    KidTask uygulamasının ana yönetici sınıfı.
    
    Attributes:
        tasks (List[Task]): Tüm görevlerin listesi
        wishes (List[Wish]): Tüm dileklerin listesi
        users (List[User]): Tüm kullanıcıların listesi
        data_dir (str): Veri dosyalarının saklanacağı dizin
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        KidTaskApp sınıfının yapıcı metodu.
        
        Args:
            data_dir (str): Veri dosyalarının saklanacağı dizin.
                          Varsayılan: "data"
        """
        self.tasks: List[Task] = []
        self.wishes: List[Wish] = []
        self.users: List[User] = []
        self.data_dir = data_dir
        
        # Veri dizinini oluştur (yoksa)
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_data(self) -> None:
        """
        Tüm veri listelerini (tasks, wishes, users) JSON formatında
        dosyalara kaydeder.
        
        Hata yönetimi:
        - IOError: Dosya yazma hatalarını yakalar ve uygun mesaj verir
        - PermissionError: Dosya izin hatalarını yakalar
        """
        try:
            # Tasks dosyasına kaydet
            tasks_file = os.path.join(self.data_dir, "tasks.json")
            with open(tasks_file, 'w', encoding='utf-8') as f:
                tasks_data = [task.to_dict() for task in self.tasks]
                json.dump(tasks_data, f, ensure_ascii=False, indent=2)
            
            # Wishes dosyasına kaydet
            wishes_file = os.path.join(self.data_dir, "wishes.json")
            with open(wishes_file, 'w', encoding='utf-8') as f:
                wishes_data = [wish.to_dict() for wish in self.wishes]
                json.dump(wishes_data, f, ensure_ascii=False, indent=2)
            
            # Users dosyasına kaydet
            users_file = os.path.join(self.data_dir, "users.json")
            with open(users_file, 'w', encoding='utf-8') as f:
                users_data = [user.to_dict() for user in self.users]
                json.dump(users_data, f, ensure_ascii=False, indent=2)
            
            print(f"Veriler başarıyla kaydedildi: {self.data_dir}")
            
        except IOError as e:
            print(f"Dosya yazma hatası: {e}")
            raise
        except PermissionError as e:
            print(f"Dosya izin hatası: {e}")
            raise
        except Exception as e:
            print(f"Beklenmeyen hata: {e}")
            raise
    
    def load_data(self) -> None:
        """
        Program başlangıcında verileri JSON dosyalarından yükler.
        
        Hata yönetimi:
        - FileNotFoundError: Dosya bulunamadığında yakalar ve uygun mesaj verir
        - IOError: Dosya okuma hatalarını yakalar
        - json.JSONDecodeError: JSON format hatalarını yakalar
        """
        try:
            # Tasks dosyasını yükle
            tasks_file = os.path.join(self.data_dir, "tasks.json")
            if os.path.exists(tasks_file):
                with open(tasks_file, 'r', encoding='utf-8') as f:
                    tasks_data = json.load(f)
                    self.tasks = [Task.from_dict(task) for task in tasks_data]
                print(f"Görevler yüklendi: {len(self.tasks)} adet")
            else:
                print("Görevler dosyası bulunamadı. Yeni liste oluşturuluyor.")
                self.tasks = []
            
            # Wishes dosyasını yükle
            wishes_file = os.path.join(self.data_dir, "wishes.json")
            if os.path.exists(wishes_file):
                with open(wishes_file, 'r', encoding='utf-8') as f:
                    wishes_data = json.load(f)
                    self.wishes = [Wish.from_dict(wish) for wish in wishes_data]
                print(f"Dilekler yüklendi: {len(self.wishes)} adet")
            else:
                print("Dilekler dosyası bulunamadı. Yeni liste oluşturuluyor.")
                self.wishes = []
            
            # Users dosyasını yükle
            users_file = os.path.join(self.data_dir, "users.json")
            if os.path.exists(users_file):
                with open(users_file, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                    self.users = [User.from_dict(user) for user in users_data]
                print(f"Kullanıcılar yüklendi: {len(self.users)} adet")
            else:
                print("Kullanıcılar dosyası bulunamadı. Yeni liste oluşturuluyor.")
                self.users = []
            
        except FileNotFoundError as e:
            print(f"Dosya bulunamadı: {e}")
            print("Yeni veri listeleri oluşturuluyor.")
            self.tasks = []
            self.wishes = []
            self.users = []
        except IOError as e:
            print(f"Dosya okuma hatası: {e}")
            print("Yeni veri listeleri oluşturuluyor.")
            self.tasks = []
            self.wishes = []
            self.users = []
        except json.JSONDecodeError as e:
            print(f"JSON format hatası: {e}")
            print("Yeni veri listeleri oluşturuluyor.")
            self.tasks = []
            self.wishes = []
            self.users = []
        except Exception as e:
            print(f"Beklenmeyen hata: {e}")
            print("Yeni veri listeleri oluşturuluyor.")
            self.tasks = []
            self.wishes = []
            self.users = []
    
    def find_user(self, username: str) -> Optional[User]:
        """
        Kullanıcı adına göre kullanıcıyı bulur.
        
        Args:
            username (str): Aranacak kullanıcı adı
            
        Returns:
            Optional[User]: Bulunan kullanıcı veya None
        """
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def find_task(self, task_id: int) -> Optional[Task]:
        """
        Görev ID'sine göre görevi bulur.
        
        Args:
            task_id (int): Aranacak görev ID'si
            
        Returns:
            Optional[Task]: Bulunan görev veya None
        """
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def find_wish(self, wish_id: int) -> Optional[Wish]:
        """
        Dilek ID'sine göre dileği bulur.
        
        Args:
            wish_id (int): Aranacak dilek ID'si
            
        Returns:
            Optional[Wish]: Bulunan dilek veya None
        """
        for wish in self.wishes:
            if wish.wish_id == wish_id:
                return wish
        return None
    
    def add_task(self, title: str, description: str, due_date: datetime, 
                 points: int, child_username: str, created_by: str) -> Task:
        """
        Yeni bir görev ekler.
        
        Args:
            title (str): Görevin başlığı
            description (str): Görevin açıklaması
            due_date (datetime): Görevin bitiş tarihi
            points (int): Görevin puan değeri
            child_username (str): Görevin atandığı çocuğun kullanıcı adı
            created_by (str): Görevi oluşturan kullanıcı adı
            
        Returns:
            Task: Oluşturulan görev nesnesi
        """
        new_task = Task(
            title=title,
            description=description,
            due_date=due_date,
            points=points,
            child_username=child_username,
            created_by=created_by
        )
        self.tasks.append(new_task)
        return new_task
    
    def approve_task(
        self,
        task_id: int,
        rating: float,
        approver_role: UserRole,
        child_username: Optional[str] = None
    ) -> None:
        """
        Bir görevi onaylar ve çocuğun puanını/seviyesini günceller.
        
        Args:
            task_id (int): Onaylanacak görevin ID'si
            rating (float): Göreve verilen puan (0-100)
            approver_role (UserRole): Onaylayan kullanıcının rolü
            child_username (Optional[str]): Görevin sahibi olan çocuğun kullanıcı adı
            
        Raises:
            ValueError: Görev bulunamazsa, onaylayıcı rolü uygun değilse
                       veya çocuk kullanıcı bulunamazsa
        """
        # Görevi bul
        task = self.find_task(task_id)
        if not task:
            raise ValueError(f"Görev bulunamadı: {task_id}")
        
        # Görevin tamamlanmış olması gerekir
        if not task.is_completed:
            raise ValueError("Görev tamamlanmadan onaylanamaz.")
        
        # Onaylayıcı rolü kontrolü (Parent veya Teacher olmalı)
        if approver_role not in [UserRole.PARENT, UserRole.TEACHER]:
            raise ValueError("Sadece Parent veya Teacher görevleri onaylayabilir.")
        
        # Görevi onayla
        task.approve(rating)
        
        # Çocuk kullanıcıyı bul ve puan/seviye güncelle
        if child_username:
            child_user = self.find_user(child_username)
            if not child_user:
                raise ValueError(f"Çocuk kullanıcı bulunamadı: {child_username}")
            
            if child_user.role != UserRole.CHILD:
                raise ValueError(f"Kullanıcı Child rolünde değil: {child_username}")
            
            # Çocuğa puan ekle
            child_user.add_points(task.points)
            
            # Çocuğa rating ekle ve seviyeyi güncelle
            child_user.add_rating(rating)
            
            print(f"Görev onaylandı. {child_username} kullanıcısına {task.points} puan eklendi.")
            print(f"Yeni toplam puan: {child_user.total_points}, Yeni seviye: {child_user.level}")
    
    def add_wish(self, description: str, cost: int, required_level: int,
                 child_username: str, wish_type: str = "product") -> Wish:
        """
        Yeni bir dilek ekler.
        
        Args:
            description (str): Dileğin açıklaması
            cost (int): Dileğin puan karşılığı (maliyeti)
            required_level (int): Dileğin görülebilmesi için gereken minimum seviye
            child_username (str): Dileği ekleyen çocuğun kullanıcı adı
            wish_type (str): Dilek tipi ("product" veya "activity")
            
        Returns:
            Wish: Oluşturulan dilek nesnesi
        """
        new_wish = Wish(
            description=description,
            cost=cost,
            required_level=required_level,
            child_username=child_username,
            wish_type=wish_type
        )
        self.wishes.append(new_wish)
        return new_wish
    
    def approve_wish(self, wish_id: int, approver_role: UserRole) -> None:
        """
        Bir dileği onaylar.
        
        Args:
            wish_id (int): Onaylanacak dileğin ID'si
            approver_role (UserRole): Onaylayan kullanıcının rolü
            
        Raises:
            ValueError: Dilek bulunamazsa veya onaylayıcı rolü uygun değilse
        """
        # Dileği bul
        wish = self.find_wish(wish_id)
        if not wish:
            raise ValueError(f"Dilek bulunamadı: {wish_id}")
        
        # Onaylayıcı rolü kontrolü (Parent veya Teacher olmalı)
        if approver_role not in [UserRole.PARENT, UserRole.TEACHER]:
            raise ValueError("Sadece Parent veya Teacher dilekleri onaylayabilir.")
        
        # Dileği onayla
        wish.approve()
        print(f"Dilek #{wish_id} onaylandı.")
    
    def __str__(self) -> str:
        """
        KidTaskApp nesnesinin string temsilini döndürür.
        
        Returns:
            str: Uygulama istatistikleri
        """
        return (f"KidTaskApp - Görevler: {len(self.tasks)}, "
                f"Dilekler: {len(self.wishes)}, Kullanıcılar: {len(self.users)}")
    
    def __repr__(self) -> str:
        """
        KidTaskApp nesnesinin resmi string temsilini döndürür.
        
        Returns:
            str: Nesnenin yapıcı çağrısına benzer temsil
        """
        return f"KidTaskApp(data_dir='{self.data_dir}')"

