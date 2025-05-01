# --- START OF FILE chess_ai.py ---

import platform
import pygame, sys
from pygame.locals import *
import os
from sys import exit
from random import *
import random
import time
import copy  # ### AI ADDITION ###: Needed for deep copying board states

# I using the UTF-8 symbols to build the board
board = ["╔═╤═╤═╤═╤═╤═╤═╤═╗",
         "║  │  │  │╲│╱│  │  │  ║",
         "╟─┼─┼─┼─┼─┼─┼─┼─╢",
         "║  │  │  │╱│╲│  │  │  ║",
         "╟─╬─┼─┼─┼─┼─┼─╬─╢",
         "║  │  │  │  │  │  │  │  ║",
         "╠─┼─╬─┼─╬─┼─╬─┼─╣",
         "║  │  │  │  │  │  │  │  ║",
         "╟─┴─┴─┴─┴─┴─┴─┴─╢",
         "║    楚    河      漢    界    ║",
         "╟─┬─┬─┬─┬─┬─┬─┬─╢",
         "║  │  │  │  │  │  │  │  ║",
         "╠─┼─╬─┼─╬─┼─╬─┼─╣",
         "║  │  │  │  │  │  │  │  ║",
         "╟─╬─┼─┼─┼─┼─┼─╬─╢",
         "║  │  │  │╲│╱│  │  │  ║",
         "╟─┼─┼─┼─┼─┼─┼─┼─╢",
         "║  │  │  │╱│╲│  │  │  ║",
         "╚═╧═╧═╧═╧═╧═╧═╧═╝",]

# using list to store the pieces
# define : NAME,COORDINATE,COLOR
# ### REFACTOR ###: Store original pieces separately for potential reset
initial_piecesBlack=[['將',(4,0),(0,0,0)],['士',(3,0),(0,0,0)],['士',(5,0),(0,0,0)],
        ['象',(2,0),(0,0,0)],['象',(6,0),(0,0,0)],
        ['馬',(1,0),(0,0,0)],['馬',(7,0),(0,0,0)],
        ['車',(0,0),(0,0,0)],['車',(8,0),(0,0,0)],
        ['砲',(1,2),(0,0,0)],['砲',(7,2),(0,0,0)],
        ['卒',(0,3),(0,0,0)],['卒',(2,3),(0,0,0)],['卒',(4,3),(0,0,0)],['卒',(6,3),(0,0,0)],['卒',(8,3),(0,0,0)],]
initial_piecesRed=[['帥',(4,9),(255,0,0)],['仕',(3,9),(255,0,0)],['仕',(5,9),(255,0,0)],
        ['相',(2,9),(255,0,0)],['相',(6,9),(255,0,0)],
        ['傌',(1,9),(255,0,0)],['傌',(7,9),(255,0,0)],
        ['俥',(0,9),(255,0,0)],['俥',(8,9),(255,0,0)],
        ['炮',(1,7),(255,0,0)],['炮',(7,7),(255,0,0)],
        ['兵',(0,6),(255,0,0)],['兵',(2,6),(255,0,0)],['兵',(4,6),(255,0,0)],['兵',(6,6),(255,0,0)],['兵',(8,6),(255,0,0)],]

piecesBlack = copy.deepcopy(initial_piecesBlack)
piecesRed = copy.deepcopy(initial_piecesRed)

# pygame for UI. keyboard and screen
pygame.init()
# ### REFACTOR ###: Slightly larger screen for messages
size = (800, 700) # Increased height
screen = pygame.display.set_mode(size)
DISPLAYSURF = screen # Use the same surface

pygame.display.set_caption('奕棋子 - Xiangqi with AI')

print (platform.system())

# different font in different platform
fontSize=28
# ### REFACTOR ###: Added fallback and error handling for font
myfont = None
try:
    if platform.system() == 'Linux':
        # Try common locations or specific installed fonts known to work
        try:
            myfont = pygame.font.SysFont("WenQuanYi Micro Hei", fontSize)
        except:
            try:
                myfont = pygame.font.SysFont("Noto Sans CJK SC", fontSize)
            except:
                myfont = pygame.font.SysFont("MingLiu", fontSize) # Fallback
    elif platform.system() == 'Windows':
        # Ensure the path exists or use a known good font
        mingliu_path = os.path.join(os.environ.get('SYSTEMROOT', 'C:\\Windows'), "Fonts\\mingliu.ttc")
        kaiu_path = os.path.join(os.environ.get('SYSTEMROOT', 'C:\\Windows'), "Fonts\\kaiu.ttf")
        if os.path.exists(mingliu_path):
             myfont = pygame.font.Font(mingliu_path, fontSize)
        elif os.path.exists(kaiu_path):
             myfont = pygame.font.Font(kaiu_path, fontSize)
        else:
             myfont = pygame.font.SysFont("SimSun", fontSize) # Common fallback
    elif platform.system() == 'Darwin': # macOS
        myfont = pygame.font.SysFont("PingFang SC", fontSize) # Common on macOS
        if not myfont:
             myfont = pygame.font.SysFont("MingLiu", fontSize) # Fallback
except Exception as e:
    print(f"Error loading preferred font: {e}")
    print("Attempting default system font.")
    myfont = pygame.font.SysFont(None, fontSize + 4) # Use default font, maybe adjust size

if myfont is None:
    print("CRITICAL: Could not load a suitable font. Exiting.")
    pygame.quit()
    sys.exit()

# Colors
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = ( 255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BOARD_COLOR = (255, 225, 128) # Piece background color

# --- Game State Variables ---
cursorX = 4
cursorY = 9
pieceTake = None # Stores the piece currently selected by the player [['name',(x,y),color], index]
valid_moves = [] # Stores valid move destinations [[x,y],...]
valid_attacks = [] # Stores valid attack destinations [[x,y],...]
current_player = 'red' # 'red' (human) or 'black' (AI)
ai_thinking = False
game_over = False
winner = None
status_message = "Red's Turn (Player)"
# ### AI ADDITION ###: AI difficulty (search depth)
AI_DEPTH = 3 # Adjust for difficulty (2=Easier, 3=Medium, 4=Harder but slower)

# --- Drawing Functions ---
def plotBoard():
    # Clear screen (or relevant part)
    screen.fill(BLACK)

    # Draw Title/Logo (simplified)
    title_surf = myfont.render('奕 棋 子', True, WHITE)
    screen.blit(title_surf,(600, fontSize))

    # Draw Board Lines
    board_start_x = fontSize
    board_start_y = fontSize * 3 # Move board down slightly for status message
    for line_index, line_text in enumerate(board):
        textsurface = myfont.render(line_text, True, WHITE)
        screen.blit(textsurface, (board_start_x, board_start_y + (line_index * fontSize)))

    # Draw Pieces
    for piece in piecesBlack + piecesRed:
        # Convert logical coordinates (0-8, 0-9) to pixel coordinates
        px = int(board_start_x + piece[1][0] * fontSize * 2 + fontSize / 2)
        py = int(board_start_y + piece[1][1] * fontSize * 2 + fontSize / 2)

        # Draw piece circle background
        pygame.draw.circle(screen, BOARD_COLOR, (px, py), int(fontSize * .9), 0)
        # Draw piece circle border
        pygame.draw.circle(screen, BLACK, (px, py), int(fontSize * .8), 1)
        # Draw piece character
        textsurface = myfont.render(piece[0], True, piece[2])
        text_rect = textsurface.get_rect(center=(px, py))
        screen.blit(textsurface, text_rect)

    # Draw Status Message
    status_surf = myfont.render(status_message, True, WHITE)
    screen.blit(status_surf, (fontSize, fontSize))

# ### REFACTOR ###: Adjusted plotCursor etc. to account for board_start_y offset
def plotCursor(x, y):
    board_start_x = fontSize
    board_start_y = fontSize * 3
    px_top_left_x = int(board_start_x + x * fontSize * 2 - fontSize/2)
    px_top_left_y = int(board_start_y + y * fontSize * 2 - fontSize/2)
    px_bottom_right_x = int(px_top_left_x + fontSize * 2)
    px_bottom_right_y = int(px_top_left_y + fontSize * 2)

    # Draw corners
    corner_len = fontSize // 3
    pygame.draw.lines(screen, RED, False, [(px_top_left_x, px_top_left_y + corner_len), (px_top_left_x, px_top_left_y), (px_top_left_x + corner_len, px_top_left_y)], 2)
    pygame.draw.lines(screen, RED, False, [(px_top_left_x, px_bottom_right_y - corner_len), (px_top_left_x, px_bottom_right_y), (px_top_left_x + corner_len, px_bottom_right_y)], 2)
    pygame.draw.lines(screen, RED, False, [(px_bottom_right_x - corner_len, px_top_left_y), (px_bottom_right_x, px_top_left_y), (px_bottom_right_x, px_top_left_y + corner_len)], 2)
    pygame.draw.lines(screen, RED, False, [(px_bottom_right_x - corner_len, px_bottom_right_y), (px_bottom_right_x, px_bottom_right_y), (px_bottom_right_x, px_bottom_right_y - corner_len)], 2)


def plotMarker(x, y, color):
    board_start_x = fontSize
    board_start_y = fontSize * 3
    px_top_left_x = int(board_start_x + x * fontSize * 2 - fontSize/2)
    px_top_left_y = int(board_start_y + y * fontSize * 2 - fontSize/2)
    px_bottom_right_x = int(px_top_left_x + fontSize * 2)
    px_bottom_right_y = int(px_top_left_y + fontSize * 2)

    # Draw simple box marker
    pygame.draw.rect(screen, color, (px_top_left_x, px_top_left_y, fontSize * 2, fontSize * 2), 2)

def plotCandidate(x, y):
    plotMarker(x, y, GREEN)

def plotAttack(x, y):
    plotMarker(x, y, YELLOW) # Changed color for better contrast

# --- Collision Detection ---
# ### REFACTOR ###: Combined detection functions, added state passing for AI simulation
def get_piece_at(x, y, p_black, p_red):
    for piece in p_black:
        if piece[1] == (x, y):
            return piece, 'black'
    for piece in p_red:
        if piece[1] == (x, y):
            return piece, 'red'
    return None, None

# --- Movement Logic (Largely unchanged, but adapted for AI state passing) ---
# ### REFACTOR ###: Pass piece lists explicitly for AI simulation
def find_valid_moves(piece, p_black, p_red):
    candidate_moves = []
    candidate_attacks = []
    pieceX, pieceY = piece[1]
    piece_color = 'black' if piece in p_black else 'red'
    opponent_pieces = p_red if piece_color == 'black' else p_black
    my_pieces = p_black if piece_color == 'black' else p_red

    # Helper function to check occupancy for simulation
    def is_occupied(x, y):
        return get_piece_at(x, y, p_black, p_red)[0] is not None

    def get_occupant_color(x, y):
        return get_piece_at(x, y, p_black, p_red)[1]

    # --- GENERAL (將 / 帥) ---
    if piece[0] in ['將', '帥']:
        palace_y_range = range(0, 3) if piece_color == 'black' else range(7, 10)
        palace_x_range = range(3, 6)
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in moves:
            nx, ny = pieceX + dx, pieceY + dy
            if nx in palace_x_range and ny in palace_y_range:
                occupant, occ_color = get_piece_at(nx, ny, p_black, p_red)
                if occupant is None:
                    candidate_moves.append([nx, ny])
                elif occ_color != piece_color:
                    candidate_attacks.append([nx, ny])
        # Flying General Rule Check (Simplified - only check direct line of sight)
        opponent_general = None
        for p in opponent_pieces:
            if p[0] in ['將', '帥']:
                opponent_general = p
                break
        if opponent_general and opponent_general[1][0] == pieceX:
            clear_path = True
            for y in range(min(pieceY, opponent_general[1][1]) + 1, max(pieceY, opponent_general[1][1])):
                 if is_occupied(pieceX, y):
                     clear_path = False
                     break
            if clear_path:
                 candidate_attacks.append(list(opponent_general[1]))


    # --- ADVISOR (士 / 仕) ---
    if piece[0] in ['士', '仕']:
        palace_y_range = range(0, 3) if piece_color == 'black' else range(7, 10)
        palace_x_range = range(3, 6)
        moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in moves:
            nx, ny = pieceX + dx, pieceY + dy
            if nx in palace_x_range and ny in palace_y_range:
                occupant, occ_color = get_piece_at(nx, ny, p_black, p_red)
                if occupant is None:
                    candidate_moves.append([nx, ny])
                elif occ_color != piece_color:
                    candidate_attacks.append([nx, ny])

    # --- ELEPHANT (象 / 相) ---
    if piece[0] in ['象', '相']:
        river_side_y = 4 if piece_color == 'black' else 5
        moves = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        for dx, dy in moves:
            nx, ny = pieceX + dx, pieceY + dy
            block_x, block_y = pieceX + dx // 2, pieceY + dy // 2 # Blocking point
            # Check bounds and river crossing
            if 0 <= nx <= 8 and 0 <= ny <= 9:
                 if (piece_color == 'black' and ny > river_side_y) or \
                    (piece_color == 'red' and ny < river_side_y):
                     continue # Cannot cross river

                 if not is_occupied(block_x, block_y):
                     occupant, occ_color = get_piece_at(nx, ny, p_black, p_red)
                     if occupant is None:
                         candidate_moves.append([nx, ny])
                     elif occ_color != piece_color:
                         candidate_attacks.append([nx, ny])

    # --- HORSE (馬 / 傌) ---
    if piece[0] in ['馬', '傌']:
        moves = [
            (1, 2, 0, 1), (-1, 2, 0, 1), # Up L
            (1, -2, 0, -1), (-1, -2, 0, -1), # Down L
            (2, 1, 1, 0), (2, -1, 1, 0), # Right L
            (-2, 1, -1, 0), (-2, -1, -1, 0) # Left L
        ]
        for dx, dy, bx, by in moves:
            nx, ny = pieceX + dx, pieceY + dy
            block_x, block_y = pieceX + bx, pieceY + by # Blocking point
            if 0 <= nx <= 8 and 0 <= ny <= 9:
                if not is_occupied(block_x, block_y):
                    occupant, occ_color = get_piece_at(nx, ny, p_black, p_red)
                    if occupant is None:
                        candidate_moves.append([nx, ny])
                    elif occ_color != piece_color:
                        candidate_attacks.append([nx, ny])

    # --- CHARIOT (車 / 俥) ---
    if piece[0] in ['車', '俥']:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = pieceX + dx, pieceY + dy
            while 0 <= nx <= 8 and 0 <= ny <= 9:
                occupant, occ_color = get_piece_at(nx, ny, p_black, p_red)
                if occupant is None:
                    candidate_moves.append([nx, ny])
                else:
                    if occ_color != piece_color:
                        candidate_attacks.append([nx, ny])
                    break # Path blocked
                nx += dx
                ny += dy

    # --- CANNON (砲 / 炮) ---
    if piece[0] in ['砲', '炮']:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = pieceX + dx, pieceY + dy
            jumped = False
            while 0 <= nx <= 8 and 0 <= ny <= 9:
                occupant, occ_color = get_piece_at(nx, ny, p_black, p_red)
                if occupant is None:
                    if not jumped:
                        candidate_moves.append([nx, ny])
                else: # Found a piece
                    if not jumped:
                        jumped = True # This is the piece to jump over
                    else:
                        # This is the target piece after jumping
                        if occ_color != piece_color:
                            candidate_attacks.append([nx, ny])
                        break # Cannot jump over more than one or attack own piece
                nx += dx
                ny += dy

    # --- PAWN (卒 / 兵) ---
    if piece[0] in ['卒', '兵']:
        if piece_color == 'black':
            forward_moves = [(0, 1)]
            if pieceY >= 5: # Across the river
                forward_moves.extend([(1, 0), (-1, 0)])
            for dx, dy in forward_moves:
                 nx, ny = pieceX + dx, pieceY + dy
                 if 0 <= nx <= 8 and 0 <= ny <= 9:
                     occupant, occ_color = get_piece_at(nx, ny, p_black, p_red)
                     if occupant is None:
                         candidate_moves.append([nx, ny])
                     elif occ_color == 'red': # Black attacks Red
                         candidate_attacks.append([nx, ny])
        else: # Red piece
            forward_moves = [(0, -1)]
            if pieceY <= 4: # Across the river
                forward_moves.extend([(1, 0), (-1, 0)])
            for dx, dy in forward_moves:
                 nx, ny = pieceX + dx, pieceY + dy
                 if 0 <= nx <= 8 and 0 <= ny <= 9:
                     occupant, occ_color = get_piece_at(nx, ny, p_black, p_red)
                     if occupant is None:
                         candidate_moves.append([nx, ny])
                     elif occ_color == 'black': # Red attacks Black
                         candidate_attacks.append([nx, ny])

    # ### AI ADDITION ### Check for moves that result in Generals facing illegally
    final_moves = []
    final_attacks = []

    for move in candidate_moves + candidate_attacks:
        is_attack = move in candidate_attacks
        target_x, target_y = move

        # Simulate the move
        temp_p_black = copy.deepcopy(p_black)
        temp_p_red = copy.deepcopy(p_red)
        current_temp_pieces = temp_p_black if piece_color == 'black' else temp_p_red
        opponent_temp_pieces = temp_p_red if piece_color == 'black' else temp_p_black

        moved_piece_copy = None
        original_index = -1

        # Find the piece in the temporary list and move it
        for i, p in enumerate(current_temp_pieces):
            if p[1] == piece[1] and p[0] == piece[0]: # Match coordinate and type
                moved_piece_copy = p
                original_index = i
                break

        if moved_piece_copy:
             moved_piece_copy[1] = (target_x, target_y)

             # Simulate capture if it's an attack move
             if is_attack:
                 captured_piece_index = -1
                 for i, opp_p in enumerate(opponent_temp_pieces):
                     if opp_p[1] == (target_x, target_y):
                         captured_piece_index = i
                         break
                 if captured_piece_index != -1:
                     del opponent_temp_pieces[captured_piece_index]

             # Check Flying General condition AFTER simulated move
             black_gen, red_gen = None, None
             for p in temp_p_black:
                 if p[0] == '將': black_gen = p; break
             for p in temp_p_red:
                 if p[0] == '帥': red_gen = p; break

             generals_face = False
             if black_gen and red_gen and black_gen[1][0] == red_gen[1][0]:
                 clear = True
                 bx, rx = black_gen[1][0], red_gen[1][0] # Should be same x
                 min_y = min(black_gen[1][1], red_gen[1][1])
                 max_y = max(black_gen[1][1], red_gen[1][1])
                 for y_check in range(min_y + 1, max_y):
                     if get_piece_at(bx, y_check, temp_p_black, temp_p_red)[0] is not None:
                         clear = False
                         break
                 if clear:
                     generals_face = True # Illegal state

             if not generals_face:
                 if is_attack:
                     final_attacks.append(move)
                 else:
                     final_moves.append(move)

    return final_moves, final_attacks


# ### AI ADDITION ###: Function to get ALL legal moves for a side
def get_all_legal_moves_for_side(p_black, p_red, side):
    all_moves = [] # Format: [piece_ref, (target_x, target_y), is_capture]
    pieces_to_check = p_black if side == 'black' else p_red

    for piece in pieces_to_check:
        moves, attacks = find_valid_moves(piece, p_black, p_red)
        for move in moves:
            all_moves.append([piece, tuple(move), False])
        for attack in attacks:
            all_moves.append([piece, tuple(attack), True])

    return all_moves

# ### AI ADDITION ###: Simple Evaluation Function
piece_values = {
    '將': 10000, '帥': 10000,
    '車': 9, '俥': 9,
    '馬': 4, '傌': 4,
    '砲': 4.5, '炮': 4.5, # Cannons slightly more valuable than horses maybe
    '象': 2, '相': 2,
    '士': 2, '仕': 2,
    '卒': 1, '兵': 1
}

def evaluate_board(p_black, p_red):
    score = 0
    # Material score
    for piece in p_black:
        val = piece_values.get(piece[0], 0)
        # Bonus for black pawns across river
        if piece[0] == '卒' and piece[1][1] > 4:
            val += 1
        score += val
    for piece in p_red:
        val = piece_values.get(piece[0], 0)
        # Bonus for red pawns across river
        if piece[0] == '兵' and piece[1][1] < 5:
            val += 1
        score -= val # Subtract red's score

    # Add mobility (simple version: count legal moves)
    # This can be computationally expensive if not optimized
    # score += 0.1 * len(get_all_legal_moves_for_side(p_black, p_red, 'black'))
    # score -= 0.1 * len(get_all_legal_moves_for_side(p_black, p_red, 'red'))

    # Checkmate/Stalemate (Basic Check - just see if a general is missing)
    black_gen_exists = any(p[0] == '將' for p in p_black)
    red_gen_exists = any(p[0] == '帥' for p in p_red)

    if not red_gen_exists: return 10000 # Black wins (very high score)
    if not black_gen_exists: return -10000 # Red wins (very low score)

    # AI plays as Black, so positive score is good for AI
    return score

# ### AI ADDITION ###: Minimax with Alpha-Beta Pruning
def minimax(p_black, p_red, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_over: # Check global game_over or depth limit
        return evaluate_board(p_black, p_red), None

    legal_moves = get_all_legal_moves_for_side(p_black, p_red, 'black' if maximizing_player else 'red')

    # Check for no legal moves (stalemate or checkmate already handled by evaluation finding missing king)
    if not legal_moves:
         return evaluate_board(p_black, p_red), None


    best_move = random.choice(legal_moves) # Default to a random move if all else fails

    if maximizing_player: # Black's turn (AI)
        max_eval = -float('inf')
        for move in legal_moves:
            piece, target_coord, is_capture = move
            # Create copies and simulate the move
            temp_p_black = copy.deepcopy(p_black)
            temp_p_red = copy.deepcopy(p_red)
            piece_original_coord = piece[1] # Store original coordinate

            moved_piece_temp = None
            piece_index = -1
            # Find the specific piece instance in the temp list
            for i, p in enumerate(temp_p_black):
                 if p[1] == piece_original_coord and p[0] == piece[0]:
                      moved_piece_temp = p
                      piece_index = i
                      break

            if moved_piece_temp:
                 moved_piece_temp[1] = target_coord # Update position
                 # Simulate capture
                 if is_capture:
                      captured_index = -1
                      for i, opp_p in enumerate(temp_p_red):
                           if opp_p[1] == target_coord:
                                captured_index = i
                                break
                      if captured_index != -1:
                           del temp_p_red[captured_index]

                 # Recursive call
                 evaluation, _ = minimax(temp_p_black, temp_p_red, depth - 1, alpha, beta, False) # Switch to minimizing player

                 if evaluation > max_eval:
                      max_eval = evaluation
                      best_move = move
                 alpha = max(alpha, evaluation)
                 if beta <= alpha:
                      break # Prune

        return max_eval, best_move
    else: # Red's turn (Human simulation)
        min_eval = float('inf')
        for move in legal_moves:
            piece, target_coord, is_capture = move
            # Create copies and simulate the move
            temp_p_black = copy.deepcopy(p_black)
            temp_p_red = copy.deepcopy(p_red)
            piece_original_coord = piece[1]

            moved_piece_temp = None
            piece_index = -1
            for i, p in enumerate(temp_p_red):
                 if p[1] == piece_original_coord and p[0] == piece[0]:
                      moved_piece_temp = p
                      piece_index = i
                      break

            if moved_piece_temp:
                moved_piece_temp[1] = target_coord # Update position
                # Simulate capture
                if is_capture:
                     captured_index = -1
                     for i, opp_p in enumerate(temp_p_black):
                         if opp_p[1] == target_coord:
                             captured_index = i
                             break
                     if captured_index != -1:
                         del temp_p_black[captured_index]

                # Recursive call
                evaluation, _ = minimax(temp_p_black, temp_p_red, depth - 1, alpha, beta, True) # Switch to maximizing player

                if evaluation < min_eval:
                     min_eval = evaluation
                     best_move = move # Keep track of the move leading to min_eval
                beta = min(beta, evaluation)
                if beta <= alpha:
                     break # Prune

        return min_eval, best_move

# ### AI ADDITION ###: Function to trigger AI move
def make_ai_move():
    global piecesBlack, piecesRed, current_player, status_message, ai_thinking, game_over, winner

    ai_thinking = True
    status_message = "Black's Turn (AI is thinking...)"
    plotBoard() # Update display to show thinking message
    plotCursor(cursorX, cursorY) # Keep cursor visible
    pygame.display.update()
    pygame.time.wait(100) # Small delay to ensure message is seen

    start_time = time.time()
    # Call minimax to find the best move for Black (AI)
    score, best_move = minimax(piecesBlack, piecesRed, AI_DEPTH, -float('inf'), float('inf'), True)
    end_time = time.time()

    ai_thinking = False

    if best_move is None:
        # This should ideally not happen if checkmate is handled correctly
        # Or it could be stalemate
        black_gen_exists = any(p[0] == '將' for p in piecesBlack)
        red_gen_exists = any(p[0] == '帥' for p in piecesRed)
        if not red_gen_exists: # Red already lost
             winner = 'Black (AI)'
        elif not black_gen_exists: # Black already lost (shouldn't happen on AI turn)
             winner = 'Red (Player)'
        else: # Stalemate? Or error
             winner = "Draw/Stalemate?"
        game_over = True
        status_message = f"Game Over! {winner}. Press ESC to exit."
        print("AI has no moves!")
        return

    # Execute the best move found by the AI
    ai_piece, target_coord, is_capture = best_move
    piece_to_move = None
    piece_index = -1

    # Find the actual piece instance in the main game list
    for i, p in enumerate(piecesBlack):
        # Match original position and type to handle identical pieces
        if p[1] == ai_piece[1] and p[0] == ai_piece[0]:
            piece_to_move = p
            piece_index = i
            break

    if piece_to_move:
        # Perform capture if needed
        if is_capture:
            captured_index = -1
            for i, red_p in enumerate(piecesRed):
                if red_p[1] == target_coord:
                    captured_index = i
                    print(f"AI captures {red_p[0]} at {target_coord}")
                    break
            if captured_index != -1:
                 # Check if captured piece is the General
                 if piecesRed[captured_index][0] == '帥':
                      winner = 'Black (AI)'
                      game_over = True
                 del piecesRed[captured_index]

        # Move the AI piece
        print(f"AI moves {piece_to_move[0]} from {piece_to_move[1]} to {target_coord}. Eval: {score:.2f}, Time: {end_time - start_time:.2f}s")
        piece_to_move[1] = target_coord


    else:
        print("Error: AI selected a piece that couldn't be found!") # Should not happen

    # Switch turn back to player
    current_player = 'red'
    if not game_over:
        status_message = "Red's Turn (Player)"
    else:
        status_message = f"Game Over! {winner}. Press ESC to exit."


# --- Main Game Loop ---
plotBoard()
plotCursor(cursorX, cursorY)
loopMain = True
while loopMain:

    # Handle AI Turn
    if current_player == 'black' and not ai_thinking and not game_over:
        make_ai_move()
        # Redraw board after AI move
        plotBoard()
        plotCursor(cursorX, cursorY) # Redraw cursor at its last position
        pygame.display.update()


    # Handle Events
    for event in pygame.event.get():
        if event.type == QUIT:
            loopMain = False
        if event.type == KEYDOWN:
            if game_over: # Only allow ESCAPE if game is over
                if event.key == K_ESCAPE:
                    loopMain = False
                continue # Ignore other keys when game over

            if current_player == 'black': # Ignore player input during AI turn
                 continue

            # Player Input Handling (Red's Turn)
            if event.key == K_UP:
                if cursorY > 0: cursorY -= 1
            elif event.key == K_DOWN:
                if cursorY < 9: cursorY += 1
            elif event.key == K_LEFT:
                if cursorX > 0: cursorX -= 1
            elif event.key == K_RIGHT:
                if cursorX < 8: cursorX += 1
            elif event.key == K_RETURN:
                target_coord = (cursorX, cursorY)

                if pieceTake is None: # --- First Enter: Select Piece ---
                    selected, color = get_piece_at(cursorX, cursorY, piecesBlack, piecesRed)
                    if selected and color == 'red': # Can only select own pieces (Red)
                        pieceTake = selected
                        valid_moves, valid_attacks = find_valid_moves(pieceTake, piecesBlack, piecesRed)
                        if not valid_moves and not valid_attacks:
                            # No valid moves for this piece, deselect
                            pieceTake = None
                            status_message = "Red's Turn: Selected piece has no moves."
                        else:
                             status_message = f"Red's Turn: Selected {pieceTake[0]}. Choose destination."

                    else:
                         status_message = "Red's Turn: Select one of your pieces (Red)."
                         pieceTake = None
                         valid_moves = []
                         valid_attacks = []

                else: # --- Second Enter: Place Piece ---
                    is_valid_move = any(m == [cursorX, cursorY] for m in valid_moves)
                    is_valid_attack = any(a == [cursorX, cursorY] for a in valid_attacks)

                    if is_valid_move or is_valid_attack:
                        # Execute Move/Attack
                        original_pos = pieceTake[1] # Store original position for log

                        # If attacking, remove the opponent's piece
                        if is_valid_attack:
                             captured_index = -1
                             for i, black_p in enumerate(piecesBlack):
                                 if black_p[1] == target_coord:
                                     captured_index = i
                                     print(f"Player captures {black_p[0]} at {target_coord}")
                                     break
                             if captured_index != -1:
                                 # Check if captured piece is the General
                                 if piecesBlack[captured_index][0] == '將':
                                     winner = 'Red (Player)'
                                     game_over = True
                                 del piecesBlack[captured_index]

                        # Move the player's piece
                        print(f"Player moves {pieceTake[0]} from {original_pos} to {target_coord}")
                        pieceTake[1] = target_coord


                        # Clear selection and switch turn
                        pieceTake = None
                        valid_moves = []
                        valid_attacks = []
                        current_player = 'black'
                        if not game_over:
                             status_message = "Black's Turn (AI)"
                        else:
                             status_message = f"Game Over! {winner}. Press ESC to exit."

                    else:
                         # Invalid destination, keep piece selected or deselect?
                         # Let's keep it selected for now
                         status_message = f"Red's Turn: Invalid move for {pieceTake[0]}. Choose valid spot or ESC."
                         # Optionally, could deselect here:
                         # pieceTake = None
                         # valid_moves = []
                         # valid_attacks = []


            elif event.key == K_ESCAPE:
                # Deselect piece if one is selected, otherwise exit (if needed)
                if pieceTake:
                    pieceTake = None
                    valid_moves = []
                    valid_attacks = []
                    status_message = "Red's Turn (Player)"
                # else: # Optional: Exit on second ESC
                #    loopMain = False


            # --- Redraw after any key press during player's turn ---
            if current_player == 'red':
                 plotBoard()
                 # Plot markers for selected piece
                 if pieceTake:
                     for move in valid_moves:
                         plotCandidate(move[0], move[1])
                     for attack in valid_attacks:
                         plotAttack(attack[0], attack[1])
                 plotCursor(cursorX, cursorY)


    # Update the display unless AI is thinking (already updated)
    if not ai_thinking:
         pygame.display.update()


# --- End of Game Loop ---
pygame.quit()
sys.exit()

# --- Keep console output for board reference if needed ---
print("╔═╤═╤═╤═╤═╤═╤═╤═╗")
# ... (rest of board printout) ...
print("╚═╧═╧═╧═╧═╧═╧═╧═╝")
# --- END OF FILE chess_ai.py ---
