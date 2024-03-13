import pygame


def main():
    pygame.init()

    main_surface = pygame.display.set_mode((3000, 500))

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break

        f = open("secret_map.txt", "r")
        data = f.readlines()
        f.close()

        for line in data:
            l = line.strip().split()
            x0 = int(l[1], 16)
            y0 = int(l[0], 16)
            pygame.draw.line(main_surface, (255, 0, 255), (x0, y0), (x0, y0), 1)

        pygame.display.flip()

    pygame.quit()


main()
