## Docker
Необходимо собрать docker образ с приложением.
- Версия ```pyhton 3.8``` или выше.
- Приложение принимает запросы на порту ```8000```.
- Необходимые зависимости описаны в файле ```requirements.txt```.
- В образ не должны попасть файлы не являющиеся частью приложения.

## Kubernetes
Запустить одну репику приложения в кубернетес кластере и полуить доступ к приложению через браузер (без использования ```port-forward```).
- Должны быть настроены ```readinessProbe```:   
  >- ```http``` запрос по пути ```/docs```    
  >- период опроса ```5с```   
  >- таймаут ```2с```   
  >- задержка перед стартом опроса ```10с```   
- Для пода необходимо описать реквесты и лимиты.
- Смонтировать том ```emptydir``` в каталог ```/uploads```

## Проверка
- Открыть swagger приложения в браузере ```http://<адрес>/docs```
- Выполнить запрос ```ping```, приложение должно ответить кодом ```200```.
- Выполнить запрос ```send_file```, который выполняет загрузку файла в приложение, приложение должно ответить кодом ```200```, внутри пода проверить наличие файла ```/uploads/filename.jpg```

-----------------------------------------------------------------------
## Запуск локально в minikube:

#### 1) Копируем проект и переходим в рабочую директорию:
```bash
git git clone https://github.com/manbojack/test-app.git --branch=v2.0
cd test-app/
```

#### 2) Запуск minikube:
```bash 
minikube start \
  && minikube addons enable ingress \
  && minikube addons enable ingress-dns \
  && minikube addons enable metrics-server
```

#### 3) Добавляем доменное имя в hosts:
```bash
sudo echo "$(minikube ip) test-app.local" >> /etc/hosts
```

#### 4) Создаём локальный docker образ для minikube:
```bash
eval $(minikube -p minikube docker-env)
docker build -t dockeraxer/test-app .
```

#### 5) Запуск Pod:
```bash
helm install test-app .helm/
```

#### 6) Открываем [swagger](http://test-app.local/docs) и выполняем запросы из пункта "Проверка"
