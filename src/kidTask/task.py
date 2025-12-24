"""
Task (Görev) sınıfı - KidTask projesi için.

Bu sınıf, çocuklara atanan görevleri temsil eder ve görevlerin
durumunu, puanlarını ve onay bilgilerini yönetir.
"""

from datetime import datetime
from typing import Optional


class Task:
    """
    Görev bilgilerini yöneten sınıf.
    
    Attributes:
        title (str): Görevin başlığı
        description (str): Görevin açıklaması
        due_date (datetime): Görevin bitiş tarihi
        points (int): Görevin puan değeri
        is_completed (bool): Görevin tamamlanıp tamamlanmadığı
        is_approved (bool): Görevin onaylanıp onaylanmadığı
        rating (Optional[float]): Göreve verilen puan/derecelendirme (0-100)
        task_id (int): Görevin benzersiz kimliği
    """
    
    _id_counter = 1
    
    def __init__(
        self,
        title: str,
        description: str,
        due_date: datetime,
        points: int,
        task_id: Optional[int] = None,
        child_username: Optional[str] = None,
        created_by: Optional[str] = None
    ):
        """
        Task sınıfının yapıcı metodu.
        
        Args:
            title (str): Görevin başlığı
            description (str): Görevin açıklaması
            due_date (datetime): Görevin bitiş tarihi
            points (int): Görevin puan değeri
            task_id (Optional[int]): Görevin benzersiz kimliği. 
                                    Belirtilmezse otomatik atanır.
            child_username (Optional[str]): Görevin atandığı çocuğun kullanıcı adı
            created_by (Optional[str]): Görevi oluşturan kullanıcı (Parent/Teacher)
        """
        self.task_id = task_id if task_id is not None else Task._id_counter
        Task._id_counter = max(Task._id_counter, self.task_id + 1)
        
        self.title = title
        self.description = description
        self.due_date = due_date
        self.points = points
        self.child_username = child_username
        self.created_by = created_by
        self.is_completed = False
        self.is_approved = False
        self.rating = None
    
    def complete(self) -> None:
        """
        Görevi tamamlandı olarak işaretler.
        """
        self.is_completed = True
    
    def approve(self, rating: float) -> None:
        """
        Görevi onaylar ve puan verir.
        
        Args:
            rating (float): Göreve verilen puan (0-100 aralığında olmalı)
        """
        if not (0 <= rating <= 100):
            raise ValueError(f"Puan 0-100 aralığında olmalıdır. Alınan değer: {rating}")
        
        if not self.is_completed:
            raise ValueError("Görev tamamlanmadan onaylanamaz.")
        
        self.is_approved = True
        self.rating = rating
    
    def to_dict(self) -> dict:
        """
        Task nesnesini dictionary formatına dönüştürür (JSON kaydetme için).
        
        Returns:
            dict: Task bilgilerini içeren dictionary
        """
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat(),
            'points': self.points,
            'child_username': self.child_username,
            'created_by': self.created_by,
            'is_completed': self.is_completed,
            'is_approved': self.is_approved,
            'rating': self.rating
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Dictionary'den Task nesnesi oluşturur (JSON yükleme için).
        
        Args:
            data (dict): Task bilgilerini içeren dictionary
            
        Returns:
            Task: Oluşturulan Task nesnesi
        """
        task = cls(
            title=data['title'],
            description=data['description'],
            due_date=datetime.fromisoformat(data['due_date']),
            points=data['points'],
            task_id=data.get('task_id'),
            child_username=data.get('child_username'),
            created_by=data.get('created_by')
        )
        task.is_completed = data.get('is_completed', False)
        task.is_approved = data.get('is_approved', False)
        task.rating = data.get('rating')
        return task
    
    def __str__(self) -> str:
        """
        Task nesnesinin string temsilini döndürür.
        
        Returns:
            str: Görevin özet bilgisi
        """
        status = "Tamamlandı ve Onaylandı" if self.is_approved else \
                 "Tamamlandı" if self.is_completed else "Devam Ediyor"
        rating_info = f", Puan: {self.rating}" if self.rating else ""
        return f"Görev #{self.task_id}: {self.title} - {status}{rating_info}"
    
    def __repr__(self) -> str:
        """
        Task nesnesinin resmi string temsilini döndürür.
        
        Returns:
            str: Nesnenin yapıcı çağrısına benzer temsil
        """
        return (f"Task(task_id={self.task_id}, title='{self.title}', "
                f"points={self.points}, is_completed={self.is_completed}, "
                f"is_approved={self.is_approved})")

