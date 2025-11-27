"""
Wish (Dilek) sınıfı - KidTask projesi için.

Bu sınıf, çocukların puan karşılığında alabilecekleri dilekleri temsil eder.
"""

from typing import Optional


class Wish:
    """
    Dilek bilgilerini yöneten sınıf.
    
    Attributes:
        description (str): Dileğin açıklaması
        cost (int): Dileğin puan karşılığı (maliyeti)
        is_approved (bool): Dileğin onaylanıp onaylanmadığı
        required_level (int): Dileğin görülebilmesi için gereken minimum seviye
        wish_id (int): Dileğin benzersiz kimliği
    """
    
    _id_counter = 1
    
    def __init__(
        self,
        description: str,
        cost: int,
        required_level: int = 1,
        wish_id: Optional[int] = None
    ):
        """
        Wish sınıfının yapıcı metodu.
        
        Args:
            description (str): Dileğin açıklaması
            cost (int): Dileğin puan karşılığı (maliyeti)
            required_level (int): Dileğin görülebilmesi için gereken minimum seviye.
                                 Varsayılan: 1
            wish_id (Optional[int]): Dileğin benzersiz kimliği. 
                                    Belirtilmezse otomatik atanır.
        """
        self.wish_id = wish_id if wish_id is not None else Wish._id_counter
        Wish._id_counter = max(Wish._id_counter, self.wish_id + 1)
        
        self.description = description
        self.cost = cost
        self.required_level = required_level
        self.is_approved = False
    
    def approve(self) -> None:
        """
        Dileği onaylar.
        """
        self.is_approved = True
    
    def is_visible_to_level(self, user_level: int) -> bool:
        """
        Dileğin belirli bir seviyedeki kullanıcıya görünür olup olmadığını kontrol eder.
        
        Args:
            user_level (int): Kullanıcının seviyesi
            
        Returns:
            bool: Dilek görünürse True, değilse False
        """
        return user_level >= self.required_level
    
    def to_dict(self) -> dict:
        """
        Wish nesnesini dictionary formatına dönüştürür (JSON kaydetme için).
        
        Returns:
            dict: Wish bilgilerini içeren dictionary
        """
        return {
            'wish_id': self.wish_id,
            'description': self.description,
            'cost': self.cost,
            'is_approved': self.is_approved,
            'required_level': self.required_level
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Wish':
        """
        Dictionary'den Wish nesnesi oluşturur (JSON yükleme için).
        
        Args:
            data (dict): Wish bilgilerini içeren dictionary
            
        Returns:
            Wish: Oluşturulan Wish nesnesi
        """
        wish = cls(
            description=data['description'],
            cost=data['cost'],
            required_level=data.get('required_level', 1),
            wish_id=data.get('wish_id')
        )
        wish.is_approved = data.get('is_approved', False)
        return wish
    
    def __str__(self) -> str:
        """
        Wish nesnesinin string temsilini döndürür.
        
        Returns:
            str: Dileğin özet bilgisi
        """
        status = "Onaylandı" if self.is_approved else "Onay Bekliyor"
        return f"Dilek #{self.wish_id}: {self.description} - {self.cost} puan - {status} (Min. Seviye: {self.required_level})"
    
    def __repr__(self) -> str:
        """
        Wish nesnesinin resmi string temsilini döndürür.
        
        Returns:
            str: Nesnenin yapıcı çağrısına benzer temsil
        """
        return (f"Wish(wish_id={self.wish_id}, description='{self.description}', "
                f"cost={self.cost}, required_level={self.required_level}, "
                f"is_approved={self.is_approved})")

