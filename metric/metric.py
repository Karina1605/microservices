import pika
import pickle

log_file = '../logs/metric_log.csv'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Объявляем очередь features
channel.queue_declare(queue='y_true')
channel.queue_declare(queue='y_pred')

y_true_cache ={}
y_pred_cache ={}


def callback_y_pred(ch, method, properties, body):
    print(f'Получен вектор признаков {body.Body}')
    if body.message_id not in y_true_cache:
        y_pred_cache[body.message_id] = body.body
    else:
        with open(log_file, 'w') as file:
            file.write(f'{body.message_id},{y_true_cache[body.message_id]},{body.body},{abs(body.body - y_true_cache[body.message_id])}\n')
            file.close()
        y_true_cache.drop(body.message_id)

def callback_y_true(ch, method, properties, body):
    print(f'Получен вектор признаков {body.Body}')
    if body.message_id not in y_pred_cache:
        y_true_cache[body.message_id] = body.body
    else:
        with open(log_file, 'w') as file:
            file.write(f'{body.message_id},{body.body},{y_pred_cache[body.message_id]},{abs(body.body - y_pred_cache[body.message_id])}\n')
            file.close()
        y_pred_cache.drop(body.message_id)

    
channel.basic_consume(
    queue='y_true',
    on_message_callback=callback_y_true,
    auto_ack=True)

channel.basic_consume(
    queue='y_pred',
    on_message_callback=callback_y_pred,
    auto_ack=True)
# Запускаем режим ожидания прихода сообщений
channel.start_consuming()