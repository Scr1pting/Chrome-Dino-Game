class SubscriptableSurface:
    def __init__(self, surface):
        self.surface = surface

    def __getitem__(self, pos):
        x, y = pos
        return self.surface.get_at((x, y))

    def __setitem__(self, pos, value):
        x, y = pos
        self.surface.set_at((x, y), value)

    def get_size(self):
        return self.surface.get_size()

    def fill(self, color):
        self.surface.fill(color)

    def blit(self, source, dest):
        self.surface.blit(source, dest)


def check_collision(img1, pos1, img2, pos2):
    # Calculate the overlapping region
    x1, y1 = pos1
    x2, y2 = pos2

    img1_width, img1_height = img1.get_size()
    img2_width, img2_height = img2.get_size()

    overlap_x_min = max(x1, x2)
    overlap_y_min = max(y1, y2)
    overlap_x_max = min(x1 + img1_width, x2 + img2_width)
    overlap_y_max = min(y1 + img1_height, y2 + img2_height)

    if overlap_x_min >= overlap_x_max or overlap_y_min >= overlap_y_max:
        # No overlap
        return False

    # Check for overlapping non-transparent pixels
    for x in range(overlap_x_min, overlap_x_max):
        for y in range(overlap_y_min, overlap_y_max):
            img1_pixel_x = x - x1
            img1_pixel_y = y - y1
            img2_pixel_x = x - x2
            img2_pixel_y = y - y2

            img1_subscriptable = SubscriptableSurface(img1)
            img2_subscriptable = SubscriptableSurface(img2)

            img1_pixel = img1_subscriptable[img1_pixel_x, img1_pixel_y]
            img2_pixel = img2_subscriptable[img2_pixel_x, img2_pixel_y]


            # Check if both pixels are non-transparent (alpha != 0)
            if img1_pixel[3] > 100 and img2_pixel[3] > 100:
                return True

    return False
