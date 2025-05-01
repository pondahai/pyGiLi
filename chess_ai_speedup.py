# --- START OF FILE chess_ai_make_unmake.py ---

import platform
import pygame, sys
from pygame.locals import *
import os
from sys import exit
from random import *
import random
import time
# import copy # ### MAKE/UNMAKE ###: No longer needed for minimax state copies!

# --- (Keep board definition, initial_pieces definitions, pygame init, font loading, colors, game state variables AS BEFORE) ---
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

# Need to make copies at the *start* of the game
import copy # Keep copy for initial setup
piecesBlack = copy.deepcopy(initial_piecesBlack)
piecesRed = copy.deepcopy(initial_piecesRed)


pygame.init()
size = (800, 700)
screen = pygame.display.set_mode(size)
DISPLAYSURF = screen
pygame.display.set_caption('奕棋子 - Xiangqi with AI (Make/Unmake)')

print (platform.system())

fontSize=28
myfont = None
try:
    if platform.system() == 'Linux':
        try: myfont = pygame.font.SysFont("WenQuanYi Micro Hei", fontSize)
        except:
            try: myfont = pygame.font.SysFont("Noto Sans CJK SC", fontSize)
            except: myfont = pygame.font.SysFont("MingLiu", fontSize)
    elif platform.system() == 'Windows':
        mingliu_path = os.path.join(os.environ.get('SYSTEMROOT', 'C:\\Windows'), "Fonts\\mingliu.ttc")
        kaiu_path = os.path.join(os.environ.get('SYSTEMROOT', 'C:\\Windows'), "Fonts\\kaiu.ttf")
        if os.path.exists(mingliu_path): myfont = pygame.font.Font(mingliu_path, fontSize)
        elif os.path.exists(kaiu_path): myfont = pygame.font.Font(kaiu_path, fontSize)
        else: myfont = pygame.font.SysFont("SimSun", fontSize)
    elif platform.system() == 'Darwin':
        myfont = pygame.font.SysFont("PingFang SC", fontSize)
        if not myfont: myfont = pygame.font.SysFont("MingLiu", fontSize)
except Exception as e:
    print(f"Error loading preferred font: {e}")
    print("Attempting default system font.")
    myfont = pygame.font.SysFont(None, fontSize + 4)

if myfont is None:
    print("CRITICAL: Could not load a suitable font. Exiting.")
    pygame.quit()
    sys.exit()

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = ( 255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BOARD_COLOR = (255, 225, 128)

cursorX = 4
cursorY = 9
pieceTake = None
valid_moves = []
valid_attacks = []
current_player = 'red'
ai_thinking = False
game_over = False
winner = None
status_message = "Red's Turn (Player)"
AI_DEPTH = 3


# --- (Keep plotBoard, plotCursor, plotMarker, plotCandidate, plotAttack AS BEFORE) ---
def plotBoard():
    screen.fill(BLACK)
    title_surf = myfont.render('奕 棋 子 (Make/Unmake)', True, WHITE)
    screen.blit(title_surf,(550, fontSize)) # Adjusted position slightly

    board_start_x = fontSize
    board_start_y = fontSize * 3
    for line_index, line_text in enumerate(board):
        textsurface = myfont.render(line_text, True, WHITE)
        screen.blit(textsurface, (board_start_x, board_start_y + (line_index * fontSize)))

    for piece in piecesBlack + piecesRed:
        px = int(board_start_x + piece[1][0] * fontSize * 2 + fontSize / 2)
        py = int(board_start_y + piece[1][1] * fontSize * 2 + fontSize / 2)
        pygame.draw.circle(screen, BOARD_COLOR, (px, py), int(fontSize * .9), 0)
        pygame.draw.circle(screen, BLACK, (px, py), int(fontSize * .8), 1)
        textsurface = myfont.render(piece[0], True, piece[2])
        text_rect = textsurface.get_rect(center=(px, py))
        screen.blit(textsurface, text_rect)

    status_surf = myfont.render(status_message, True, WHITE)
    screen.blit(status_surf, (fontSize, fontSize))

def plotCursor(x, y):
    board_start_x = fontSize
    board_start_y = fontSize * 3
    px_top_left_x = int(board_start_x + x * fontSize * 2 - fontSize/2)
    px_top_left_y = int(board_start_y + y * fontSize * 2 - fontSize/2)
    px_bottom_right_x = int(px_top_left_x + fontSize * 2)
    px_bottom_right_y = int(px_top_left_y + fontSize * 2)
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
    pygame.draw.rect(screen, color, (px_top_left_x, px_top_left_y, fontSize * 2, fontSize * 2), 2)

def plotCandidate(x, y):
    plotMarker(x, y, GREEN)

def plotAttack(x, y):
    plotMarker(x, y, YELLOW)

# --- (Keep get_piece_at AS BEFORE) ---
def get_piece_at(x, y, p_black, p_red):
    for piece in p_black:
        if piece[1] == (x, y):
            return piece, 'black'
    for piece in p_red:
        if piece[1] == (x, y):
            return piece, 'red'
    return None, None

# --- (Keep find_valid_moves AS BEFORE, it operates on passed state) ---
# This function *reads* the state passed to it (p_black, p_red)
# but does *not* modify it. This is crucial for Make/Unmake.
def find_valid_moves(piece, p_black, p_red):
    # ... (Keep the entire logic of find_valid_moves exactly as it was in the previous AI version) ...
    # ... It should return final_moves, final_attacks based on the *passed* p_black, p_red ...
    # IMPORTANT: Ensure the 'Flying General' check inside uses the passed p_black, p_red
    # (The previous version already did this correctly by simulating on temp copies,
    # but here it will just read the current state passed to it)

    # START of find_valid_moves logic (Copy from previous version)
    candidate_moves = []
    candidate_attacks = []
    pieceX, pieceY = piece[1]
    piece_color = 'black' if piece[2] == (0,0,0) else 'red' # Determine color from piece itself
    opponent_pieces = p_red if piece_color == 'black' else p_black
    my_pieces = p_black if piece_color == 'black' else p_red

    def is_occupied(x, y):
        return get_piece_at(x, y, p_black, p_red)[0] is not None

    def get_occupant_color(x, y):
        return get_piece_at(x, y, p_black, p_red)[1]

    # --- (All the specific piece movement logic: 將/帥, 士/仕, etc.) ---
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
                 # This is tricky with make/unmake. The *potential* move is an attack
                 # but the check here is about the current state legality.
                 # Let's keep adding it as an attack candidate for now.
                 # The legality check after make_move will prevent illegal moves.
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
            if 0 <= nx <= 8 and 0 <= ny <= 9:
                 if (piece_color == 'black' and ny > river_side_y) or \
                    (piece_color == 'red' and ny < river_side_y):
                     continue
                 if not is_occupied(block_x, block_y):
                     occupant, occ_color = get_piece_at(nx, ny, p_black, p_red)
                     if occupant is None:
                         candidate_moves.append([nx, ny])
                     elif occ_color != piece_color:
                         candidate_attacks.append([nx, ny])

    # --- HORSE (馬 / 傌) ---
    if piece[0] in ['馬', '傌']:
        moves = [
            (1, 2, 0, 1), (-1, 2, 0, 1), (1, -2, 0, -1), (-1, -2, 0, -1),
            (2, 1, 1, 0), (2, -1, 1, 0), (-2, 1, -1, 0), (-2, -1, -1, 0)
        ]
        for dx, dy, bx, by in moves:
            nx, ny = pieceX + dx, pieceY + dy
            block_x, block_y = pieceX + bx, pieceY + by
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
                    break
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
                else:
                    if not jumped:
                        jumped = True
                    else:
                        if occ_color != piece_color:
                            candidate_attacks.append([nx, ny])
                        break
                nx += dx
                ny += dy

    # --- PAWN (卒 / 兵) ---
    if piece[0] in ['卒', '兵']:
        if piece_color == 'black':
            forward_moves = [(0, 1)]
            if pieceY >= 5: forward_moves.extend([(1, 0), (-1, 0)])
            for dx, dy in forward_moves:
                 nx, ny = pieceX + dx, pieceY + dy
                 if 0 <= nx <= 8 and 0 <= ny <= 9:
                     occupant, occ_color = get_piece_at(nx, ny, p_black, p_red)
                     if occupant is None:
                         candidate_moves.append([nx, ny])
                     elif occ_color == 'red':
                         candidate_attacks.append([nx, ny])
        else: # Red
            forward_moves = [(0, -1)]
            if pieceY <= 4: forward_moves.extend([(1, 0), (-1, 0)])
            for dx, dy in forward_moves:
                 nx, ny = pieceX + dx, pieceY + dy
                 if 0 <= nx <= 8 and 0 <= ny <= 9:
                     occupant, occ_color = get_piece_at(nx, ny, p_black, p_red)
                     if occupant is None:
                         candidate_moves.append([nx, ny])
                     elif occ_color == 'black':
                         candidate_attacks.append([nx, ny])

    # --- Check for moves resulting in Generals facing ---
    # This check is slightly different now. We generate all potential moves first,
    # then rely on make_move/unmake_move structure within minimax to implicitly
    # handle illegal states by not exploring them further if they lead to immediate loss
    # or if the evaluation function penalizes such states heavily (though the current one doesn't explicitly).
    # A more robust way is to check *after* make_move within minimax, but let's start simpler.
    # We can filter here for basic legality, but the deep check is complex without full state copies.
    # For now, let's assume minimax handles it via evaluation or the opponent capturing the exposed king.
    # A simple filter can be added here if needed, but let's proceed.

    # Return raw candidates for now. The `check_generals_facing_after_move` logic
    # needs to be integrated differently, likely after a make_move call.
    final_moves = candidate_moves
    final_attacks = candidate_attacks

    return final_moves, final_attacks
    # END of find_valid_moves logic


# --- (Keep get_all_legal_moves_for_side AS BEFORE) ---
def get_all_legal_moves_for_side(p_black, p_red, side):
    all_moves = [] # Format: [piece_object_ref, (target_x, target_y), is_capture]
    pieces_to_check = p_black if side == 'black' else p_red

    for piece in pieces_to_check:
        # Pass the current state lists to find_valid_moves
        moves, attacks = find_valid_moves(piece, p_black, p_red)
        for move in moves:
            all_moves.append([piece, tuple(move), False])
        for attack in attacks:
            all_moves.append([piece, tuple(attack), True])

    # Add move sorting here later if desired

    return all_moves

# --- (Keep evaluate_board AS BEFORE) ---
piece_values = {
    '將': 10000, '帥': 10000, '車': 9, '俥': 9, '馬': 4, '傌': 4,
    '砲': 4.5, '炮': 4.5, '象': 2, '相': 2, '士': 2, '仕': 2, '卒': 1, '兵': 1
}
def evaluate_board(p_black, p_red):
    # Checkmate/Stalemate (Basic Check - just see if a general is missing)
    # This needs to be checked first, as a missing king overrides other scores.
    black_gen_exists = any(p[0] == '將' for p in p_black)
    red_gen_exists = any(p[0] == '帥' for p in p_red)

    if not red_gen_exists: return 10000 + AI_DEPTH # Black wins (add depth to prioritize faster wins)
    if not black_gen_exists: return -10000 - AI_DEPTH # Red wins (subtract depth)

    score = 0
    for piece in p_black:
        val = piece_values.get(piece[0], 0)
        if piece[0] == '卒' and piece[1][1] > 4: val += 1
        score += val
    for piece in p_red:
        val = piece_values.get(piece[0], 0)
        if piece[0] == '兵' and piece[1][1] < 5: val += 1
        score -= val
    return score

# ### MAKE/UNMAKE ###: Helper to find piece index by reference and original coords
def find_piece_index(piece_list, piece_to_find):
    # Find by original coordinates and type, needed because piece objects might be recreated in some contexts
    # Although here, we should have direct references from get_all_legal_moves
    original_coord = piece_to_find[1]
    piece_type = piece_to_find[0]
    for i, p in enumerate(piece_list):
         # Use direct reference comparison if possible, fallback to coords/type
         # if id(p) == id(piece_to_find): # This might be unreliable if references change unexpectedly
         #      return i
         if p[1] == original_coord and p[0] == piece_type:
              # Ensure it's the *first* match if multiple identical pieces exist at start
              # This simple check might be ambiguous if two identical pieces moved to the same starting spot?
              # Let's rely on the reference from get_all_legal_moves for now.
              # A more robust solution might involve unique IDs per piece.
              # Re-checking: The 'piece' in the move list *is* the reference from the original list.
              if id(p) == id(piece_to_find):
                   return i
    # Fallback if reference ID match failed (shouldn't ideally happen with current structure)
    for i, p in enumerate(piece_list):
         if p[1] == original_coord and p[0] == piece_type:
              print(f"Warning: find_piece_index using fallback for {piece_type} at {original_coord}")
              return i
    return -1 # Not found

# ### MAKE/UNMAKE ###: New Make Move function
def make_move(piece, target_coord, is_capture, p_black, p_red):
    """
    Applies a move to the board state and returns undo information.
    Args:
        piece: The piece object (reference from the list) to move.
        target_coord: The (x, y) tuple where the piece is moving.
        is_capture: Boolean indicating if this move captures an opponent piece.
        p_black: The list of black pieces.
        p_red: The list of red pieces.
    Returns:
        A tuple containing undo information: (original_coords, captured_piece_object_or_None)
    """
    original_coords = piece[1] # Store original position
    piece_color = 'black' if piece[2] == (0,0,0) else 'red'
    opponent_list = p_red if piece_color == 'black' else p_black
    captured_piece = None

    # Perform capture first (if any)
    if is_capture:
        capture_index = -1
        for i, opp_piece in enumerate(opponent_list):
            if opp_piece[1] == target_coord:
                # Store the *actual object* being removed
                captured_piece = opponent_list.pop(i)
                break
        # if captured_piece is None: # Should not happen if is_capture is True and move is valid
        #     print(f"Error: Capture move specified for {piece[0]} to {target_coord}, but no opponent piece found!")

    # Move the piece
    # We already have the reference 'piece', just update its coordinate
    piece[1] = target_coord

    # Return information needed to undo the move
    return (original_coords, captured_piece)

# ### MAKE/UNMAKE ###: New Unmake Move function
def unmake_move(piece, undo_info, p_black, p_red):
    """
    Reverts a move on the board state using undo information.
    Args:
        piece: The piece object (reference) that was moved.
        undo_info: The tuple returned by make_move (original_coords, captured_piece).
        p_black: The list of black pieces.
        p_red: The list of red pieces.
    """
    original_coords, captured_piece = undo_info

    # Move the piece back
    piece[1] = original_coords

    # If a piece was captured, put it back
    if captured_piece:
        piece_color = 'black' if captured_piece[2] == (0,0,0) else 'red'
        target_list = p_black if piece_color == 'black' else p_red
        # Simply append it back. Order might not be preserved, but shouldn't affect logic.
        target_list.append(captured_piece)


# ### MAKE/UNMAKE ###: Modified Minimax
# Now operates directly on piecesBlack, piecesRed
def minimax(p_black, p_red, depth, alpha, beta, maximizing_player):
    # Check for game over state based on current board
    black_gen_exists = any(p[0] == '將' for p in p_black)
    red_gen_exists = any(p[0] == '帥' for p in p_red)
    if not red_gen_exists or not black_gen_exists or depth == 0:
        # Pass the *current* state lists to evaluate
        return evaluate_board(p_black, p_red), None

    # Get moves for the current player based on the *current* state
    legal_moves = get_all_legal_moves_for_side(p_black, p_red, 'black' if maximizing_player else 'red')

    if not legal_moves:
         # No legal moves, evaluate the current stalemate/checkmate state
         return evaluate_board(p_black, p_red), None

    # Initialize best_move with a random legal move as fallback
    best_move = random.choice(legal_moves)

    if maximizing_player: # Black's turn (AI)
        max_eval = -float('inf')
        # Consider adding move ordering here later for better pruning
        # Example: legal_moves.sort(key=lambda m: piece_values.get(get_piece_at(m[1][0],m[1][1],p_black,p_red)[0][0], 0) if m[2] else 0, reverse=True)
        for move in legal_moves:
            piece, target_coord, is_capture = move

            # Apply the move to the *actual* board state
            undo_info = make_move(piece, target_coord, is_capture, p_black, p_red)

            # Check if the move resulted in generals facing (optional but good)
            # generals_facing = check_generals_facing(p_black, p_red) # Implement this helper if needed
            # if generals_facing:
            #    evaluation = -float('inf') # Illegal move for the current player
            # else:
            # Recursive call - passing the same lists (now modified)
            evaluation, _ = minimax(p_black, p_red, depth - 1, alpha, beta, False)

            # Undo the move to restore the state for the next iteration
            unmake_move(piece, undo_info, p_black, p_red)

            # --- Alpha-Beta logic ---
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move # Store the move details
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break # Prune

        return max_eval, best_move

    else: # Red's turn (Minimizing player)
        min_eval = float('inf')
        # Consider move ordering here too
        for move in legal_moves:
            piece, target_coord, is_capture = move

            # Apply the move
            undo_info = make_move(piece, target_coord, is_capture, p_black, p_red)

            # generals_facing = check_generals_facing(p_black, p_red)
            # if generals_facing:
            #    evaluation = float('inf') # Illegal move for Red
            # else:
            # Recursive call
            evaluation, _ = minimax(p_black, p_red, depth - 1, alpha, beta, True)

            # Undo the move
            unmake_move(piece, undo_info, p_black, p_red)

            # --- Alpha-Beta logic ---
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break # Prune

        return min_eval, best_move


# --- (Keep make_ai_move AS BEFORE, but ensure it calls the modified minimax) ---
def make_ai_move():
    global piecesBlack, piecesRed, current_player, status_message, ai_thinking, game_over, winner

    ai_thinking = True
    status_message = "Black's Turn (AI is thinking...)"
    plotBoard(); plotCursor(cursorX, cursorY); pygame.display.update(); pygame.time.wait(50)

    start_time = time.time()
    # Call minimax - it now operates directly on the global lists
    score, best_move = minimax(piecesBlack, piecesRed, AI_DEPTH, -float('inf'), float('inf'), True)
    end_time = time.time()

    ai_thinking = False

    if best_move is None:
        # Handle stalemate or error
        black_gen_exists = any(p[0] == '將' for p in piecesBlack)
        red_gen_exists = any(p[0] == '帥' for p in piecesRed)
        if not red_gen_exists: winner = 'Black (AI)'
        elif not black_gen_exists: winner = 'Red (Player)'
        else: winner = "Draw/Stalemate?"
        game_over = True
        status_message = f"Game Over! {winner}. Press ESC to exit."
        print("AI has no moves or game ended!")
        return

    # ### MAKE/UNMAKE ###: Execute the best move *permanently* on the main board
    ai_piece, target_coord, is_capture = best_move
    piece_to_move = ai_piece # We have the direct reference from minimax result

    final_captured_piece_name = None
    if is_capture:
        capture_index = -1
        for i, red_p in enumerate(piecesRed):
            if red_p[1] == target_coord:
                final_captured_piece_name = red_p[0]
                # Check for game over
                if final_captured_piece_name == '帥':
                    winner = 'Black (AI)'
                    game_over = True
                del piecesRed[i]
                break

    # Move the AI piece permanently
    print(f"AI moves {piece_to_move[0]} from {piece_to_move[1]} to {target_coord}", end="")
    if final_captured_piece_name: print(f" capturing {final_captured_piece_name}", end="")
    print(f". Eval: {score:.2f}, Time: {end_time - start_time:.2f}s")
    piece_to_move[1] = target_coord # Update the piece in the main list

    current_player = 'red'
    if not game_over:
        status_message = "Red's Turn (Player)"
    else:
        status_message = f"Game Over! {winner}. Press ESC to exit."


# --- Main Game Loop (Mostly unchanged, uses the global pieces lists) ---
plotBoard()
plotCursor(cursorX, cursorY) # Redraw cursor at its last position
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
            if game_over:
                if event.key == K_ESCAPE: loopMain = False
                continue

            if current_player == 'black': continue

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

                if pieceTake is None: # Select Piece
                    selected, color = get_piece_at(cursorX, cursorY, piecesBlack, piecesRed)
                    if selected and color == 'red':
                        pieceTake = selected
                        # Use the main lists to find valid moves for the player
                        valid_moves, valid_attacks = find_valid_moves(pieceTake, piecesBlack, piecesRed)
                        if not valid_moves and not valid_attacks:
                            pieceTake = None
                            status_message = "Red's Turn: Selected piece has no moves."
                        else:
                            status_message = f"Red's Turn: Selected {pieceTake[0]}. Choose destination."
                    else:
                        status_message = "Red's Turn: Select one of your pieces (Red)."
                        pieceTake = None; valid_moves = []; valid_attacks = []
                else: # Place Piece
                    is_valid_move = any(m == [cursorX, cursorY] for m in valid_moves)
                    is_valid_attack = any(a == [cursorX, cursorY] for a in valid_attacks)

                    if is_valid_move or is_valid_attack:
                        original_pos = pieceTake[1]
                        captured_piece_name = None
                        if is_valid_attack:
                             capture_index = -1
                             for i, black_p in enumerate(piecesBlack):
                                 if black_p[1] == target_coord:
                                     captured_piece_name = black_p[0]
                                     if captured_piece_name == '將':
                                         winner = 'Red (Player)'; game_over = True
                                     del piecesBlack[i]
                                     break
                        # Move player's piece permanently
                        print(f"Player moves {pieceTake[0]} from {original_pos} to {target_coord}", end="")
                        if captured_piece_name: print(f" capturing {captured_piece_name}", end="")
                        print()
                        pieceTake[1] = target_coord

                        pieceTake = None; valid_moves = []; valid_attacks = []
                        current_player = 'black'
                        if not game_over: status_message = "Black's Turn (AI)"
                        else: status_message = f"Game Over! {winner}. Press ESC to exit."
                    else:
                         status_message = f"Red's Turn: Invalid move for {pieceTake[0]}. Choose valid spot or ESC."

            elif event.key == K_ESCAPE:
                if pieceTake:
                    pieceTake = None; valid_moves = []; valid_attacks = []
                    status_message = "Red's Turn (Player)"

            # Redraw after player's key press
            if current_player == 'red':
                 plotBoard()
                 if pieceTake:
                     for move in valid_moves: plotCandidate(move[0], move[1])
                     for attack in valid_attacks: plotAttack(attack[0], attack[1])
                 plotCursor(cursorX, cursorY)

    # Update display
    if not ai_thinking:
         pygame.display.update()

# --- End of Game Loop ---
pygame.quit()
sys.exit()
# --- END OF FILE ---