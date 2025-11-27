"""
User (Kullanıcı) sınıfı - KidTask projesi için.

Bu sınıf, uygulamadaki tüm kullanıcıları (Child, Parent, Teacher) temsil eder.
"""

from typing import Optional
from enum import Enum


class UserRole(Enum):
    """Kullanıcı rolleri için enum sınıfı."""
    CHILD = "Child"
    PARENT = "Parent"
    TEACHER = "Teacher"


class User:
    """
    Kullanıcı bilgilerini yöneten sınıf.
    
    Attributes:
        username (str): Kullanıcı adı
        role (UserRole): Kullanıcının rolü (Child, Parent, Teacher)
        password (str): Kullanıcı şifresi
        total_points (Optional[int]): Toplam puan (sadece Child kullanıcıları için)
        level (Optional[int]): Kullanıcı seviyesi (sadece Child kullanıcıları için)
        ratings (list): Tamamlanan görevlerin puanlarını tutan liste (Child için)
    """
    
    def __init__(
        self,
        username: str,
        role: UserRole,
        password: str,
        total_points: Optional[int] = None,
        level: Optional[int] = None,
        ratings: Optional[list] = None
    ):
        """
        User sınıfının yapıcı metodu.
        
        Args:
            username (str): Kullanıcı adı
            role (UserRole): Kullanıcının rolü
            password (str): Kullanıcı şifresi
            total_points (Optional[int]): Toplam puan (Child için)
            level (Optional[int]): Kullanıcı seviyesi (Child için)
            ratings (Optional[list]): Başlangıç puan listesi (Child için)
        """
        self.username = username
        self.role = role if isinstance(role, UserRole) else UserRole(role)
        self.password = password
        
        # Child kullanıcıları için özel özellikler
        if self.role == UserRole.CHILD:
            self.total_points = total_points if total_points is not None else 0
            self.ratings = ratings if ratings is not None else []
            self.level = level if level is not None else self._calculate_level()
        else:
            self.total_points = None
            self.ratings = None
            self.level = None
    
    def _calculate_level(self) -> int:
        """
        Çocuğun seviyesini, ratings listesindeki puanların ortalamasına
        göre dinamik olarak hesaplar.
        
        Seviye belirleme kriterleri:
        - Ortalama 0-40: Level 1
        - Ortalama 41-70: Level 2
        - Ortalama 71-100: Level 3
        
        Returns:
            int: Hesaplanan seviye (1, 2 veya 3)
        """
        try:
            if not self.ratings or len(self.ratings) == 0:
                return 1
            
            average_rating = sum(self.ratings) / len(self.ratings)
            
            if 0 <= average_rating <= 40:
                return 1
            elif 41 <= average_rating <= 70:
                return 2
            elif 71 <= average_rating <= 100:
                return 3
            else:
                return 1
                
        except ZeroDivisionError:
            return 1
    
    def update_level(self) -> int:
        """
        Çocuğun seviyesini günceller (sadece Child kullanıcıları için).
        
        Returns:
            int: Güncellenmiş seviye
        """
        if self.role != UserRole.CHILD:
            raise ValueError("Sadece Child kullanıcıları için seviye güncellenebilir.")
        
        self.level = self._calculate_level()
        return self.level
    
    def add_points(self, points: int) -> None:
        """
        Çocuğa puan ekler (sadece Child kullanıcıları için).
        
        Args:
            points (int): Eklenecek puan miktarı
        """
        if self.role != UserRole.CHILD:
            raise ValueError("Sadece Child kullanıcıları için puan eklenebilir.")
        
        self.total_points += points
    
    def add_rating(self, rating: float) -> None:
        """
        Çocuğa yeni bir görev puanı ekler ve seviyeyi otomatik günceller.
        
        Args:
            rating (float): Eklenecek görev puanı (0-100 aralığında olmalı)
        """
        if self.role != UserRole.CHILD:
            raise ValueError("Sadece Child kullanıcıları için puan eklenebilir.")
        
        if not (0 <= rating <= 100):
            raise ValueError(f"Puan 0-100 aralığında olmalıdır. Alınan değer: {rating}")
        
        self.ratings.append(rating)
        self.update_level()
    
    def get_average_rating(self) -> float:
        """
        Mevcut puanların ortalamasını hesaplar (sadece Child kullanıcıları için).
        
        Returns:
            float: Ortalama puan. Eğer liste boşsa 0.0 döner.
        """
        if self.role != UserRole.CHILD:
            raise ValueError("Sadece Child kullanıcıları için ortalama hesaplanabilir.")
        
        if not self.ratings or len(self.ratings) == 0:
            return 0.0
        return sum(self.ratings) / len(self.ratings)
    
    def to_dict(self) -> dict:
        """
        User nesnesini dictionary formatına dönüştürür (JSON kaydetme için).
        
        Returns:
            dict: User bilgilerini içeren dictionary
        """
        data = {
            'username': self.username,
            'role': self.role.value,
            'password': self.password
        }
        
        if self.role == UserRole.CHILD:
            data['total_points'] = self.total_points
            data['level'] = self.level
            data['ratings'] = self.ratings
        
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """
        Dictionary'den User nesnesi oluşturur (JSON yükleme için).
        
        Args:
            data (dict): User bilgilerini içeren dictionary
            
        Returns:
            User: Oluşturulan User nesnesi
        """
        role = UserRole(data['role'])
        return cls(
            username=data['username'],
            role=role,
            password=data['password'],
            total_points=data.get('total_points'),
            level=data.get('level'),
            ratings=data.get('ratings')
        )
    
    def __str__(self) -> str:
        """
        User nesnesinin string temsilini döndürür.
        
        Returns:
            str: Kullanıcının özet bilgisi
        """
        info = f"Kullanıcı: {self.username} ({self.role.value})"
        if self.role == UserRole.CHILD:
            info += f" - Toplam Puan: {self.total_points}, Seviye: {self.level}"
        return info
    
    def __repr__(self) -> str:
        """
        User nesnesinin resmi string temsilini döndürür.
        
        Returns:
            str: Nesnenin yapıcı çağrısına benzer temsil
        """
        return (f"User(username='{self.username}', role={self.role.value}, "
                f"total_points={self.total_points}, level={self.level})")

