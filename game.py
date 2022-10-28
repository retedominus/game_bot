from telegram import ReplyKeyboardRemove
from service import token

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)


board = list(range(1, 10))
x = chr(10060)
o = chr(11093)
count = 9
player = x
CHOICE = 0


def show_board(field):
    ch = ''
    for i in range(len(field)):
        if not i % 3:
            ch += f'\n{"-" * 25}\n'
        ch += f'{field[i]:^8}'
    ch += f"\n{'-' * 25}"
    return ch


def check_win(field):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    n = [field[x[0]] for x in win_coord if field[x[0]] == field[x[1]] == field[x[2]]]
    return n[0] if n else n


def start(update, _):
    global player, count
    board = list(range(1, 10))
    count = 9
    player = x
    update.message.reply_text("Привет, это игра называется крестики-нолики. Хотите сыграть?\n")
    update.message.reply_text(show_board(board))
    update.message.reply_text(f'Первым ходит {chr(10060)}')
    return CHOICE


def choice(update, _):
    global player, count
    move = update.message.text
    move = int(move)
    if move not in board:
        update.message.reply_text(f"Неправильный ввод{chr(9940)}\n\nПопробуйте снова")
    else:
        board.insert(board.index(move), player)
        board.remove(move)
        update.message.reply_text(show_board(board))
        if check_win(board):
            update.message.reply_text(f"{player} - Победитель!!!{chr(127942)}{chr(127881)}")
            return ConversationHandler.END
        player = o if player == x else x
        count -= 1

    if count == 0:
        update.message.reply_text(f"Ничья {chr(129309)}")
        return ConversationHandler.END


def cancel(update, _):
    update.message.reply_text('До свидания', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater(token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={CHOICE: [MessageHandler(Filters.text, choice)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    print('server start')

    updater.start_polling()
    updater.idle()
