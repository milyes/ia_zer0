# pixel_guard.py - IA_ZER0.10 - Native Pixel-Level Spatial Guardrail
# Version pure Python standard - Zéro dépendance (No-pip)
class NativePixelGuard:
    def __init__(self):
        self.gaussian_kernel_3x3 = [
            [1/16, 2/16, 1/16],
            [2/16, 4/16, 2/16],
            [1/16, 2/16, 1/16]
        ]

    def apply_convolution(self, image_matrix: list[list[int]]) -> list[list[int]]:
        hauteur = len(image_matrix)
        largeur = len(image_matrix[0]) if hauteur > 0 else 0
        if hauteur < 3 or largeur < 3:
            return image_matrix
        image_filtree = [[0] * largeur for _ in range(hauteur)]
        for y in range(1, hauteur - 1):
            for x in range(1, largeur - 1):
                somme_pixels = 0.0
                for ky in range(3):
                    for kx in range(3):
                        pixel_voisin = image_matrix[y + (ky - 1)][x + (kx - 1)]
                        poids_noyau = self.gaussian_kernel_3x3[ky][kx]
                        somme_pixels += pixel_voisin * poids_noyau
                image_filtree[y][x] = min(255, max(0, int(somme_pixels)))
        return image_filtree
