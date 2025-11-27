"""
Child (Çocuk) sınıfı - KidTask projesi için.

Bu sınıf, çocukların görev tamamlama puanlarını takip eder ve
performanslarına göre seviyelerini dinamik olarak hesaplar.
"""


class Child:
    """
    Çocuk bilgilerini ve görev puanlarını yöneten sınıf.
    
    Attributes:
        name (str): Çocuğun adı
        ratings (list): Tamamlanan görevlerin puanlarını tutan liste
        level (str): Çocuğun mevcut seviyesi (Level 1, Level 2, Level 3)
    """
    
    def __init__(self, name: str, ratings: list = None):
        """
        Child sınıfının yapıcı metodu.
        
        Args:
            name (str): Çocuğun adı
            ratings (list, optional): Başlangıç puan listesi. 
                                     Varsayılan olarak boş liste.
        """
        self.name = name
        self.ratings = ratings if ratings is not None else []
        self.level = None
        # İlk seviye hesaplamasını yap
        self.update_level()
    
    def update_level(self) -> str:
        """
        Çocuğun seviyesini, ratings listesindeki puanların ortalamasına
        göre dinamik olarak hesaplar ve günceller.
        
        Seviye belirleme kriterleri:
        - Ortalama 0-40: Level 1
        - Ortalama 41-70: Level 2
        - Ortalama 71-100: Level 3
        
        Returns:
            str: Güncellenmiş seviye bilgisi
            
        Raises:
            ZeroDivisionError: Ratings listesi boş olduğunda yakalanır
                               ve uygun bir mesaj döndürülür.
        """
        try:
            # Ratings listesinin boş olup olmadığını kontrol et
            if not self.ratings:
                self.level = "Level 1 (Henüz görev tamamlanmamış)"
                return self.level
            
            # Ortalama puanı hesapla
            average_rating = sum(self.ratings) / len(self.ratings)
            
            # Ortalama puanına göre seviyeyi belirle
            if 0 <= average_rating <= 40:
                self.level = "Level 1"
            elif 41 <= average_rating <= 70:
                self.level = "Level 2"
            elif 71 <= average_rating <= 100:
                self.level = "Level 3"
            else:
                # Puan aralığı dışındaysa varsayılan olarak Level 1
                self.level = "Level 1 (Geçersiz puan aralığı)"
            
            return self.level
            
        except ZeroDivisionError:
            # Bu durum aslında yukarıdaki if kontrolü ile önlenmiş olsa da,
            # ekstra güvenlik için hata yakalama mekanizması
            self.level = "Level 1 (Henüz görev tamamlanmamış)"
            return self.level
    
    def add_rating(self, rating: float) -> None:
        """
        Yeni bir görev puanı ekler ve seviyeyi otomatik olarak günceller.
        
        Args:
            rating (float): Eklenecek görev puanı (0-100 aralığında olmalı)
        """
        if 0 <= rating <= 100:
            self.ratings.append(rating)
            self.update_level()
        else:
            raise ValueError(f"Puan 0-100 aralığında olmalıdır. Alınan değer: {rating}")
    
    def get_average_rating(self) -> float:
        """
        Mevcut puanların ortalamasını hesaplar.
        
        Returns:
            float: Ortalama puan. Eğer liste boşsa 0.0 döner.
        """
        if not self.ratings:
            return 0.0
        return sum(self.ratings) / len(self.ratings)
    
    def __str__(self) -> str:
        """
        Child nesnesinin string temsilini döndürür.
        
        Returns:
            str: Çocuğun adı, seviyesi ve ortalama puanı
        """
        average = self.get_average_rating()
        return f"Çocuk: {self.name}, Seviye: {self.level}, Ortalama Puan: {average:.2f}"
    
    def __repr__(self) -> str:
        """
        Child nesnesinin resmi string temsilini döndürür.
        
        Returns:
            str: Nesnenin yapıcı çağrısına benzer temsil
        """
        return f"Child(name='{self.name}', ratings={self.ratings})"

