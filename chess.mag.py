import sys
import os
import pygame
import chess

# Obtém o diretório atual do script ou do .exe
if getattr(sys, 'frozen', False):
    current_directory = sys._MEIPASS
else:
    current_directory = os.path.dirname(os.path.abspath(__file__))

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da janela
window_width = 670  # Largura da janela
window_height = 610  # Altura da janela
screen = pygame.display.set_mode((window_width, window_height))

# Defina o título da janela
pygame.display.set_caption("chess.mag")

# Carregue a imagem do ícone e defina como ícone da janela
icon = pygame.image.load(os.path.join(current_directory, 'Assets', 'chess.mag.png'))
pygame.display.set_icon(icon)

# Defina o tamanho dos quadrados do tabuleiro
square_size = window_height // 8

# Largura da aba de indicação de turno (reduzida pela metade)
turn_indicator_width = 70

# Crie um tabuleiro de xadrez vazio
chess_board = [[' ' for _ in range(8)] for _ in range(8)]

# Defina as peças no tabuleiro
chess_board[0] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
chess_board[1] = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
chess_board[6] = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
chess_board[7] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

# Carregue imagens de peças de xadrez da pasta "Assets" e redimensione-as para o tamanho correto
piece_images = {
    'R': pygame.transform.scale(pygame.image.load(os.path.join(current_directory, 'Assets', 'white_rook.png')), (square_size, square_size)),
    'N': pygame.transform.scale(pygame.image.load(os.path.join(current_directory, 'Assets', 'white_knight.png')), (square_size, square_size)),
    'B': pygame.transform.scale(pygame.image.load(os.path.join(current_directory, 'Assets', 'white_bishop.png')), (square_size, square_size)),
    'Q': pygame.transform.scale(pygame.image.load(os.path.join(current_directory, 'Assets', 'white_queen.png')), (square_size, square_size)),
    'K': pygame.transform.scale(pygame.image.load(os.path.join(current_directory, 'Assets', 'white_king.png')), (square_size, square_size)),
    'P': pygame.transform.scale(pygame.image.load(os.path.join(current_directory, 'Assets', 'white_pawn.png')), (square_size, square_size)),
    'r': pygame.transform.scale(pygame.image.load(os.path.join(current_directory, 'Assets', 'black_rook.png')), (square_size, square_size)),
    'n': pygame.transform.scale(pygame.image.load(os.path.join(current_directory, 'Assets', 'black_knight.png')), (square_size, square_size)),
    'b': pygame.transform.scale(pygame.image.load(os.path.join(current_directory, 'Assets', 'black_bishop.png')), (square_size, square_size)),
    'q': pygame.transform.scale(pygame.image.load(os.path.join(current_directory, 'Assets', 'black_queen.png')), (square_size, square_size)),
    'k': pygame.transform.scale(pygame.image.load(os.path.join(current_directory, 'Assets', 'black_king.png')), (square_size, square_size)),
    'p': pygame.transform.scale(pygame.image.load(os.path.join(current_directory, 'Assets', 'black_pawn.png')), (square_size, square_size))
}

# Coordenadas para rastrear a peça atualmente sendo arrastada
dragging_piece = None
start_pos = None

# Variável para indicar a vez do jogador (True para brancas, False para negras)
white_turn = True

# Função para converter as coordenadas do mouse em posições do tabuleiro
def mouse_to_board(x, y):
    row = y // square_size
    col = x // square_size
    return row, col

# Função para exibir mensagens na tela
def display_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
    screen.blit(text, text_rect)

# Função para promover um peão
def promote_pawn(row, col):
    # Exibe a escolha de peças para o jogador
    promotion_options = ['Q', 'R', 'B', 'N']  # Rainha, Torre, Bispo, Cavalo
    promotion = None
    while promotion not in promotion_options:
        display_message("Escolha a peça para promoção: Q (Rainha), R (Torre), B (Bispo), N (Cavalo)")
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode in promotion_options:
                    promotion = event.unicode

    # Promove o peão para a peça escolhida
    chess_board[row][col] = promotion

# Loop principal
running = True
board = chess.Board()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo do mouse (clique)
                x, y = pygame.mouse.get_pos()
                row, col = mouse_to_board(x, y)
                piece = chess_board[row][col]
                if piece != ' ' and ((white_turn and piece.isupper()) or (not white_turn and piece.islower())):
                    if piece.lower() == 'p' and ((white_turn and row == 0) or (not white_turn and row == 7)):
                        # Peão atingiu a última fila, promove
                        promote_pawn(row, col)
                    else:
                        dragging_piece = piece
                        start_pos = (row, col)
                        chess_board[row][col] = ' '  # Remova a peça do tabuleiro

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging_piece:  # Botão esquerdo do mouse (solte)
                x, y = pygame.mouse.get_pos()
                row, col = mouse_to_board(x, y)
                end_pos = (row, col)
                move_uci = f"{chr(start_pos[1] + ord('a'))}{8 - start_pos[0]}{chr(end_pos[1] + ord('a'))}{8 - end_pos[0]}"
                try:
                    move = chess.Move.from_uci(move_uci)
                    if move in board.legal_moves:
                        chess_board[row][col] = dragging_piece
                        dragging_piece = None
                        white_turn = not white_turn  # Troca a vez do jogador
                        board.push(move)

                        # Após a verificação da jogada válida, verifique o xeque-mate
                        if board.is_checkmate():
                            if white_turn:
                                display_message("Xeque-mate! As peças pretas venceram!")
                            else:
                                display_message("Xeque-mate! As peças brancas venceram!")
                    else:
                        chess_board[start_pos[0]][start_pos[1]] = dragging_piece
                        dragging_piece = None
                except ValueError:
                    chess_board[start_pos[0]][start_pos[1]] = dragging_piece
                    dragging_piece = None

    screen.fill((255, 255, 255))

    for row in range(8):
        for col in range(8):
            color = (255, 206, 158) if (row + col) % 2 == 0 else (209, 139, 71)
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

            piece = chess_board[row][col]
            if piece != ' ':
                piece_image = piece_images[piece]
                screen.blit(piece_image, (col * square_size, row * square_size))

    # Se estivermos arrastando uma peça, desenhe-a na posição do mouse
    if dragging_piece:
        x, y = pygame.mouse.get_pos()
        screen.blit(piece_images[dragging_piece], (x - square_size // 2, y - square_size // 2))

    # Desenhe a aba indicando a vez do jogador
    turn_indicator_rect = pygame.Rect(window_width - turn_indicator_width, 0, turn_indicator_width, window_height)
    turn_indicator_color = (255, 255, 255) if white_turn else (0, 0, 0)  # Preto para a vez das negras
    pygame.draw.rect(screen, turn_indicator_color, turn_indicator_rect)

    # Desenhe o círculo na aba de indicação de turno
    turn_circle_radius = 15
    turn_circle_center = (window_width - turn_indicator_width // 2, window_height // 2)
    pygame.draw.circle(screen, turn_indicator_color, turn_circle_center, turn_circle_radius)

    pygame.display.flip()

# Encerre o Pygame
pygame.quit()
sys.exit()