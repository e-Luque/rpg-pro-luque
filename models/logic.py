class Raza:
    def __init__(self, nombre, vida_extra, fuerza):
        self.nombre = nombre
        self.vida_extra = vida_extra
        self.fuerza = fuerza

class ClaseRPG:
    def __init__(self, nombre, skill_principal):
        self.nombre = nombre
        self.skill_principal = skill_principal

class Guerrero(ClaseRPG):
    def __init__(self):
        super().__init__("Guerrero", "Ataque Físico")
        self.multiplicador_daño = 1.5

class Mago(ClaseRPG):
    def __init__(self):
        super().__init__("Mago", "Hechizo")
        self.multiplicador_magico = 2.0


