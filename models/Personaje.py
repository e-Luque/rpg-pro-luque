class Personaje:
    def __init__(self, db_data, raza_obj, clase_obj):
        self.id = db_data[0]
        self.nombre = db_data[1]
        self.nivel = db_data[2]
        self.vida = db_data[5]
        self.raza = raza_obj
        self.clase = clase_obj

    def calcular_ataque_base(self):
        factor = getattr(self.clase, 'multiplicador_daño', 1.0)
        if hasattr(self.clase, 'multiplicador_magico'):
            factor = self.clase.multiplicador_magico

        return self.nivel * factor + self.raza.fuerza