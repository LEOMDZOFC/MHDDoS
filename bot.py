import select
import requests
import threading
import re
import random
import time
import socket
from datetime import datetime
import urllib.parse
SOCKS_VERSION = 5
inviteD= False

def Decrypted_id(id_value):
    url = f"https://polydevapi.vercel.app/decrypt_id?id={id_value}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("decrypted_id")
    else:
        return f"{id_value}"

def send_spam(player_id):
    if not player_id.isdigit():
        print("Error: The player_id must contain numbers only.")
        return
    
    url = f"https://lovely-moral-asp.ngrok-free.app/api/spam_squad?id={player_id}"
    response = requests.get(url)

    if response.status_code == 200:
        print("Request was successful")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")


def telegram(message):
    token = '7740554704:AAEPp6tP2XPW5O5yZy47JbQg8CbY66Sg4uk'
    chat_id = '-1002267070288'
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Mensagem enviada com sucesso!!")
    else:
        print("Falha ao enviar mensagem")

def send_telegram_message(message):
    time.sleep(0.2)
    try:
        telegram(message)
    except KeyError as e:
        print("Error parsing data:", e)
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_player_personal_show(id, client_socket, client_id):
    url = f"https://ffinfo-server.vercel.app/v1/api/playerinfo?uid={id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        basic_info = data.get("basicInfo", {})
        social_info = data.get("socialInfo", {})
        game_info = data.get("gameInfo", {})
        pet_info = data.get("petInfo", {})
        
        account_id = basic_info.get("accountId", "desconhecido")
        create_at = basic_info.get("createAt", "desconhecido")
        last_login_at = basic_info.get("lastLoginAt", "desconhecido")
        level = basic_info.get("level", "desconhecido")
        liked = basic_info.get("liked", "desconhecido")
        nickname = basic_info.get("nickname", "desconhecido")
        region = basic_info.get("region", "desconhecido")
        
        gender = social_info.get("gender", "desconhecido")
        if gender == "Gender_MALE":
            gender = "homem"
        elif gender == "Gender_FEMALE":
            gender = "mulher"
        
        language = social_info.get("language", "desconhecido")
        if language.startswith("Language_"):
            language = language.replace("Language_", "")
        
        signature = social_info.get("signature", "desconhecido")
        
        booya_pass_level = basic_info.get("badgeCnt", "desconhecido")
        pet_name = pet_info.get("name", "desconhecido")
        
        if create_at != "desconhecido":
            create_at = datetime.utcfromtimestamp(create_at).strftime('%Y-%m-%d %H:%M:%S')
        if last_login_at != "desconhecido":
            last_login_at = datetime.utcfromtimestamp(last_login_at).strftime('%Y-%m-%d %H:%M:%S')
        
        info = (
            f"[{generate_random_color()}][c][b]-----------------------------------\n\n"
            f"[00FF00][c][b]إNome do jogador : [DC143C]{nickname}\n\n"
            f"[00FF00][c][b]Nível do jogador: [DC143C]{level}\n\n"
            f"[00FF00][c][b]Número de curtidas : [DC143C]{liked}\n\n"
            f"[00FF00][c][b]Servidor : [DC143C]{region}\n\n"
            f"[00FF00][c][b]Sexo : [DC143C]{gender}\n\n"
            f"[00FF00][c][b]a linguagem : [DC143C]{language}\n\n"
            f"[00FF00][c][b]Biografia : [DC143C]{signature}\n\n"
            f"[00FF00][c][b]Data de criação da conta : [DC143C]{create_at}\n\n"
            f"[00FF00][c][b]Última data de login : [DC143C]{last_login_at}\n\n"
            f"[00FF00][c][b]Nível de tinta : [DC143C]{booya_pass_level}\n\n"
            f"[00FF00][c][b]bicho de estimação: [DC143C]{pet_name}\n\n"
            f"[{generate_random_color()}][c][b]-----------------------------------"
        )
        
        client_socket.send(bytes.fromhex(GenResponsMsg(client_id, info)))
    else:
        return "Falha ao buscar dados"


def get_player_info(player_id, client_socket, client_id):
    url = f"https://ffinfo-server.vercel.app/v1/api/playerinfo?uid={player_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        nickname = data.get("basicInfo", {}).get("nickname", "Not_found")
        message = (
        f"[ff7f50][c][b]-----------------------------------\n\n"
        f"[{generate_random_color()}][c][b]O jogador foi adicionado. : \n\n"
        f"[FFFFFF][c][b]{nickname} \n[{generate_random_color()}][c][b] Para sua lista de amigos \n\n"
        f"[ff7f50][c][b]-----------------------------------"
        )
        client_socket.send(bytes.fromhex(GenResponsMsg(client_id, message)))
    
    except requests.exceptions.RequestException as e:
        print(f"حدث خطأ: {e}")
def Fake_Friend(id, client_socket):
    url = f"https://polydevapi.vercel.app/fake"
    response = requests.post(url, data={'target_id': id})
    
    if response.status_code == 200:
        #return response.text
        client_socket.send(bytes.fromhex(response.text))
    else:
        print(f"Request failed. Status code: {response.status_code}")
        return None

def antidetection(var):
	return var

def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color_hex = "{:02X}{:02X}{:02X}".format(r, g, b)
    return color_hex

def GenResponsMsg(player_id, message):
    encoded_message = urllib.parse.quote(message)
    url = f"https://polydevapi.vercel.app/generate"
    response = requests.post(url, data={'player_id': player_id, 'msg': encoded_message})
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Request failed. Status code: {response.status_code}")
        return None
        

def random_emote(number):
    url = f"https://polydevapi.vercel.app/random_emote?number={number}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        encrypted_emote = data.get("encrypted_emote")
        return encrypted_emote
    else:
        print(f"Ocorreu um erro, status da resposta: {response.status_code}")
        return None

def dance(id, dance_nbr=None):
    emote = random_emote(dance_nbr) if dance_nbr is not None else "c1fab8b103"
    return f"050000002008{id}100520162a1408{id}10{emote}2a0608{id}"


def ResponseMsg(info,client_socket, client_id):
    time.sleep(0.2)
    try:
        client_socket.send(bytes.fromhex(GenResponsMsg(client_id, info)))
    except KeyError as e:
        print("Error parsing data:", e)
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


class Proxy:
    def __init__(self):
        self.username = "LEOBOTFF"
        self.password = "VIP"
        self.website = "https://api-ghost.vercel.app/FFcrypto/{id}"
    def spam__invite(self,data, remote):
        global invit_spam
        while invit_spam:
            try:
               for _ in range(5):
                   remote.send(data)
                   time.sleep(0.04)
               time.sleep(0.2)
            except:
                   pass

    def Encrypt_ID(self, id):
        api_url = self.website.format(id=id)
        
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.text
            else:
                print("Falha ao buscar dados. Código de status", response.status_code)
                return None
        except requests.RequestException as e:
            print("Falha na solicitação:", e)
            return None

    def handle_client(self, connection):
        version, nmethods = connection.recv(2)

        methods = self.get_available_methods(nmethods, connection)

        if 2 not in set(methods):
            connection.close()
            return

        connection.sendall(bytes([SOCKS_VERSION, 2]))

        if not self.verify_credentials(connection):
            return

        version, cmd, _, address_type = connection.recv(4)

        if address_type == 1:
            address = socket.inet_ntoa(connection.recv(4))
        elif address_type == 3:
            domain_length = connection.recv(1)[0]
            address = connection.recv(domain_length)
            address = socket.gethostbyname(address)

        port = int.from_bytes(connection.recv(2), 'big', signed=False)

        try:
            if cmd == 1:
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.connect((address, port))
                bind_address = remote.getsockname()
            else:
                connection.close()

            addr = int.from_bytes(socket.inet_aton(bind_address[0]), 'big', signed=False)
            port = bind_address[1]

            reply = b''.join([
                SOCKS_VERSION.to_bytes(1, 'big'),
                int(0).to_bytes(1, 'big'),
                int(0).to_bytes(1, 'big'),
                int(1).to_bytes(1, 'big'),
                addr.to_bytes(4, 'big'),
                port.to_bytes(2, 'big')
            ])
        except Exception as e:
            reply = self.generate_failed_reply(address_type, 5)

        connection.sendall(reply)

        if reply[1] == 0 and cmd == 1:
            self.exchange_loop(connection, remote)

        connection.close()
        
    
    def gen_squad6(self):
        ent_packet = f'050000032708{self.EncryptedPlayerid}100520082a9a0608dbdcd7cb251a910608{self.EncryptedPlayerid}12024d4518012005329d0508{self.EncryptedPlayerid}121ee28094cd9ecd9fcd9ee29885efbcb6efbca5efbcaeefbcafefbcade385a41a024d4520ebdd88b90628363087cbd1303832421880c38566949be061e1cea561b793e66080a89763e5bfce64480150d60158991468b7db8dae037a05ab93c5b00382011f08d1daf1eb0412054f75656973180420d487d4f0042a0808cc9d85f304100392010b0107090a0b12191a1e20229801db01a0014fc00101d001ada48aaf03e80101880203920208c205d628ae2db202aa02050801109c44aa0208080210ea3018c413aa0208080f10d836188827aa0205081710bd33aa0205082b10e432aa0205083910a070aa0205083d10c16faa02050849108439aa0205081810d836aa0205081a10d836aa0205081c10d836aa0205082010d836aa0205082210d836aa0205082110d836aa0205082310d836aa0205083110e432aa0205084110d836aa0205084d10e432aa0205081b10d836aa0205083410d836aa0205082810e432aa0205082910e432c202cd0112041a0201041a730848121301040506070203f1a802f4a802f2a802f3a8021a0b080110031886032086ac021a0b0802100418810420c59a081a0b0803100418da0620ecb4051a06080520f5ec021a0d08f1a802100318b80320def0041a0d08f2a802100318bc0520d0e90a1a0d08f3a802100318ef032092c9051a1208501201631a0b0863100e188f0420eeba0d1a1b0851120265661a09086520a6910128e7021a08086620822d289e05221f121d65ed0e890ed9049103f503ad02f90abd05e907a1068507cd08950ab109d802a6a38daf03ea020410011801f202080885cab5ee01105c8a0300920300980398e0b3af0ba20319efbca334e385a4eaa884e385a4efbcb4efbca5efbca1efbcada80368b00301c2030a081c100f180320052801e203014fea03003a011a403e50056801721e313733303239333438313635343436323834305f6c646a72387477723378880180909beaf3d18fd919a20100b001e201ea010449444331fa011e313733303239333438313635343436363239355f6f747735637831756c6d050000031e08{self.EncryptedPlayerid}1005203a2a910608{self.EncryptedPlayerid}12024d4518012005329d0508{self.EncryptedPlayerid}121ee28094cd9ecd9fcd9ee29885efbcb6efbca5efbcaeefbcafefbcade385a41a024d4520ebdd88b90628363087cbd1303832421880c38566949be061e1cea561b793e66080a89763e5bfce64480150d60158991468b7db8dae037a05ab93c5b00382011f08d1daf1eb0412054f75656973180420d487d4f0042a0808cc9d85f304100392010b0107090a0b12191a1e20229801db01a0014fc00101d001ada48aaf03e80101880203920208c205d628ae2db202aa02050801109c44aa0208080210ea3018c413aa0208080f10d836188827aa0205081710bd33aa0205082b10e432aa0205083910a070aa0205083d10c16faa02050849108439aa0205081810d836aa0205081a10d836aa0205081c10d836aa0205082010d836aa0205082210d836aa0205082110d836aa0205082310d836aa0205083110e432aa0205084110d836aa0205084d10e432aa0205081b10d836aa0205083410d836aa0205082810e432aa0205082910e432c202cd0112041a0201041a730848121301040506070203f1a802f4a802f2a802f3a8021a0b080110031886032086ac021a0b0802100418810420c59a081a0b0803100418da0620ecb4051a06080520f5ec021a0d08f1a802100318b80320def0041a0d08f2a802100318bc0520d0e90a1a0d08f3a802100318ef032092c9051a1208501201631a0b0863100e188f0420eeba0d1a1b0851120265661a09086520a6910128e7021a08086620822d289e05221f121d65ed0e890ed9049103f503ad02f90abd05e907a1068507cd08950ab109d802a6a38daf03ea020410011801f202080885cab5ee01105c8a0300920300980398e0b3af0ba20319efbca334e385a4eaa884e385a4efbcb4efbca5efbca1efbcada80368b00301c2030a081c100f180320052801e203014fea03003a011a403e50056801721e313733303239333438313635343436323834305f6c646a72387477723378880180909beaf3d18fd919a20100b001e201ea010449444331fa011e313733303239333438313635343436363239355f6f747735637831756c6d'
        self.sock0500.send(bytes.fromhex(ent_packet))
    
    def invisible(self):
        ent_packet = f"050000030608{self.target_id}100520082af90508{self.target_id}1af00508{self.EncryptedPlayerid}12024d451801200432f50408{self.EncryptedPlayerid}1211e385a4e1b49ce1b498e385a4e1afa4ccb81a024d4520a4fda7b40628423084cbd13042188993e660c0bcce64e796a361fb9ae061948b8866e8b6ce64480150d70158851568e4b58fae037a0a9cd2cab00392d0f2b20382012608efdaf1eb04120cd8afd98ad8b1d8acd8a7d985180720f087d4f0042a0808ca9d85f304100392010b010307090a0b12191a1e209801dd01a0017fba010b08d6f9e6a202100118d702c00101e80105f0010e880203920208ae2d8d15ba29b810aa0208080110cc3a18a01faa0208080210f02e188827aa020a080f108e781888272001aa0205081710a14faa0205081810df31aa0205081c108f31aa0205082010c430aa0205082110cb30aa0205082210dd31aa0205082b10f02eaa0205083110f02eaa0205084910f936aa0205081a108e78aa02050823108e78aa02050839108e78aa0205083d108e78aa02050841108e78aa0205084d10e432aa0205081b108e78aa02050834108e78aa0205082810e432aa0205082910e432c2026012031a01011a3f084812110104050607f1a802f4a802f2a802f3a8021a0d08f1a802100318ec0220c3ca011a0d08f2a802100318940320a3e8041a0a08f3a802100220fec2011a0508501201631a060851120265662209120765890eed0ed904d802a8a38daf03ea020410011801f2020b0883cab5ee0110b00218018a030092032a0a13080310f906180f201528f0bbacb40632024d450a13080610a50e180f200a28f0bbacb40632024d459803fdb4b4b20ba203044d454523a80368b00302b80301c203080828100118032001c20308081a100f1803200cca030a0801109b85b5b4061801ca030a080910abf6b0b4061801d003013a011a403e50056801721e313732303331393634393738313931313136365f616471383367366864717801820103303b30880180e0aee990ede78e19a20100b00114ea010449444331fa011e313732303331393634393738313931353431355f317475736c316869396a"
        self.sock0500.send(bytes.fromhex(ent_packet))
        
    def exchange_loop(self, client, remote):
        global inviteD, hide
        hide = None
        while True:
            r, w, e = select.select([client, remote], [], [])

            if client in r:
                dataC = client.recv(4096)
                if "39699" in str(remote):
                    self.op = remote
                if "39801" in str(remote):
                    self.xz = remote
                if '0515' in dataC.hex()[0:4] and len(dataC.hex()) >= 141:
                    #print('Successfully')

                    hide = True
                    if hide == True:
                        print('hide is true ')
                        #return hide
                if '0515' in dataC.hex()[0:4] and len(dataC.hex()) >= 820 and inviteD == True:
                    for i in range(2):
                        for _ in range(5):
                            remote.send(dataC)
                            time.sleep(0.04)
                            time.sleep(0.2)
                if remote.send(dataC) <= 0:
                    break

            if remote in r:
                data = remote.recv(4096)
                if '1200' in data.hex()[0:4] and b'GroupID' in data:
                    pass
                else:
                    if '1200' in data.hex()[:4]:
                        start_marker = "08"
                        end_marker = "10"
                        start_index = data.hex().find(start_marker) + len(start_marker)
                        end_index = data.hex().find(end_marker, start_index)
                        if start_index != -1 and end_index != -1:
                            enc_client_id = data.hex()[start_index:end_index]
                            self.EncryptedPlayerid = enc_client_id
                            self.target_id = self.Encrypt_ID(8763797454)
                if "0500" in data.hex()[:4]:
                    self.sock0500 = client
                
                if '1200' in data.hex()[0:4] and b'/dance' in data:
                	i = re.split('/dance', str(data))[1]
                	id = str(i).split('(\\x')[0].strip()
                	if '***' in id:
                		id = id.replace('***', '106')
                	message = (
                	f"[ff7f50][c][b]-----------------------------------\n\n"
                	f"[{generate_random_color()}][c][b]Número de dança ativado : \n\n"
                	f"[ffffff][c][b]{id}\n\n"
                	f"[ff7f50][c][b]-----------------------------------"
                	)
                	threading.Thread(target=ResponseMsg,args=(message,client, self.EncryptedPlayerid)).start()
                	self.sock0500.send(bytes.fromhex(dance(self.EncryptedPlayerid,id)))
                	message_telegram = f"User_id = {Decrypted_id(self.EncryptedPlayerid)}\ncomando_usado  = dance\nemote_number = {id}"
                	threading.Thread(target=send_telegram_message,args=(message_telegram,)).start()
                if '1200' in data.hex()[0:4] and b'/inv' in data:
                        inviteD = True
                        message = (
                        f"[ff7f50][c][b]-----------------------------------\n\n"
                        f"[{generate_random_color()}][c][b]O spam de convites está habilitado. \n\n"
                        f"[ff7f50][c][b]-----------------------------------"
                        )
                        threading.Thread(target=ResponseMsg,args=(message,client, self.EncryptedPlayerid)).start()
                if '1200' in data.hex()[0:4] and b'/info' in data:
                        i = re.split('/info', str(data))[1]
                        id = str(i).split('(\\x')[0].strip()
                        if '***' in id:
                        	id = id.replace('***', '106')
                        message = (
                        f"[ff7f50][c][b]-----------------------------------\n\n"
                        f"[{generate_random_color()}][c][b]Extraindo informações do jogador : \n\n"
                        f"[ffffff][c][b]{id}"
                        f"\n\n[ff7f50][c][b]-----------------------------------"
                        )
                        threading.Thread(target=ResponseMsg,args=(message,client, self.EncryptedPlayerid)).start()
                        threading.Thread(target=get_player_personal_show,args=(id,client, self.EncryptedPlayerid)).start()
                        message_telegram = f"User_id = {Decrypted_id(self.EncryptedPlayerid)}\ncomando_usado = info\ntarget_id = {id}"
                        threading.Thread(target=send_telegram_message,args=(message_telegram,)).start()
                if '1200' in data.hex()[0:4] and b"/help" in data:
                    
                    like = antidetection("/like12345678")
                    spam = antidetection("/spam12345678")
                    info = antidetection("/info12345678")
                    visit = antidetection("/visit12345678")
                    fake_friend = antidetection("/id12345678")
                    seq_5 = antidetection("/5")
                    seq_6 = antidetection("/6")
                    seq_3 = antidetection("/3")
                    emote = antidetection("/dance")
                    spam_inv = antidetection("inv")
                    message = (
    f"[882afa][c][b]-----------------------------------\n\n"
    f"[{generate_random_color()}][c][b]Os comandos disponíveis no bot são: : \n\n"
    f"[2afa35][c][b]Informações do jogador   : \n"
    f"[42e6f5][b]\n"
    f"/info12345678\n\n"
    f"[2afa35][c][b] Amigo imaginário: \n"
    f"[42e6f5][b]\n"
    f"/id12345678\n"
    f"[2afa35][b]\n"
    f"[2afa35][c][b]Para converter o esquadrão para 5 pessoas   :\n\n"
    f"[42e6f5][c][b]/5\n\n"
    f"[2afa35][c][b] Para equipe de transferência de 6 pessoas    : \n"
    f"[42e6f5][c][b]/6\n\n"
    f"[2afa35][c][b]Para ativar danças : [{generate_random_color()}][c][b]\n\n"
    f"[{generate_random_color()}][c][b]/dance\n"
    f"[{generate_random_color()}][b]\n"
    f"/dance1     /dance2     -->  11 \n\n"
    f"[2afa35][c][b]Para enviar convites de spam para participar   : \n"
    f"[42e6f5][c][b]\n"
    f"ON              /inv\n\n"
    f"OFF           /-inv\n\n"
    f"[882afa][c][b]-----------------------------------\n\n"
    f"[ffff00][c][b] TELEGRAM [b] LEOMODZYTB\n\n"
)
                    #threading.Thread(target=send_telegram_message,args=()).start()
                    skwad = antidetection("--12345678")
                    message2 = (
                    f"[{generate_random_color()}][c][b]Spam de convite de grupo foi adicionado por ID\n\n"
                    f"[{generate_random_color()}][c][b]مثال : \n\n{skwad}"
                    )
                    threading.Thread(target=ResponseMsg,args=(message,client, self.EncryptedPlayerid)).start()
                    #time.sleep(0.2)
                    #threading.Thread(target=ResponseMsg,args=(message2,client, self.EncryptedPlayerid)).start()
                    message_telegram = f"User_id = {Decrypted_id(self.EncryptedPlayerid)}\ncomando_usado = help"
                    threading.Thread(target=send_telegram_message,args=(message_telegram,)).start()
                if '1200' in data.hex()[0:4] and b'/-inv' in data:
                        inviteD = False
                        message = (
                        f"[ff7f50][c][b]-----------------------------------\n\n"
                        f"[{generate_random_color()}][c][b]O spam de convites foi desativado. \n\n"
                        f"[ff7f50][c][b]-----------------------------------"
                        )
                        threading.Thread(target=ResponseMsg,args=(message,client, self.EncryptedPlayerid)).start()
                        send_telegram_message(f"User_id = {Decrypted_id(self.EncryptedPlayerid)}\ncomando_usado = inv")
                if '1200' in data.hex()[0:4] and b'/id' in data:
                        i = re.split('/id', str(data))[1]
                        id = str(i).split('(\\x')[0].strip()
                        if '***' in id:
                        	id = id.replace('***', '106')
                        message = (
                        f"[ff7f50][c][b]-----------------------------------\n\n"
                        f"[{generate_random_color()}][c][b]As informações do jogador estão sendo verificadas. : \n\n"
                        f"[ffffff][c][b]{id}"
                        f"\n\n[ff7f50][c][b]-----------------------------------"
                        )
                        threading.Thread(target=ResponseMsg,args=(message,client, self.EncryptedPlayerid)).start()
                        threading.Thread(target=get_player_info,args=(id,client, self.EncryptedPlayerid)).start()
                        threading.Thread(target=Fake_Friend,args=(id,self.sock0500)).start()
                        #threading.Thread(target=send_telegram_message,args=(")).start()
                        message_telegram = f"User_id = {Decrypted_id(self.EncryptedPlayerid)}\ncomando_usado  = fake_friend\ntarget_id = {id}"
                        threading.Thread(target=send_telegram_message,args=(message_telegram,)).start()

                if '1200' in data.hex()[0:4] and b'/6' in data and 700 > len(data.hex()):
                        message = (
                        f"[ff7f50][c][b]-----------------------------------\n\n"
                        f"[{generate_random_color()}][c][b]O time foi atualizado para 6. Envie um convite para a equipe global.ة "
                        f"\n\n[ff7f50][c][b]-----------------------------------"
                        )
                        threading.Thread(target=ResponseMsg,args=(message,client, self.EncryptedPlayerid)).start()
                        threading.Thread(target=self.gen_squad6).start()
                        #threading.Thread(target=send_telegram_message,args=()).start()
                        message_telegram = f"User_id = {Decrypted_id(self.EncryptedPlayerid)}\ncomando_usado = /6"
                        threading.Thread(target=send_telegram_message,args=(message_telegram,)).start()
                        #send_telegram_message(f"User_id = {Decrypted_id(self.EncryptedPlayerid)}\ncomando_usado = /6")
                if '1200' in data.hex()[0:4] and b'/5' in data and 700 > len(data.hex()):
                        message = (
                        f"[ff7f50][c][b]-----------------------------------\n\n"
                        f"[{generate_random_color()}][c][b]O esquadrão foi atualizado para 5. Envie um convite para o mundo."
                        f"\n\n[ff7f50][c][b]-----------------------------------"
                        )
                        threading.Thread(target=ResponseMsg,args=(message,client, self.EncryptedPlayerid)).start()
                        threading.Thread(target=self.invisible).start()
                        #threading.Thread(target=send_telegram_message,args=()).start()
                        message_telegram = f"User_id = {Decrypted_id(self.EncryptedPlayerid)}\ncomando_usado = /5"
                        threading.Thread(target=send_telegram_message,args=(message_telegram,)).start()
                        #send_telegram_message(f"User_id = {Decrypted_id(self.EncryptedPlayerid)}\ncomando_usado = /5")
                if client.send(data) <= 0:
                    break

    def generate_failed_reply(self, address_type, error_number):
        return b''.join([
            SOCKS_VERSION.to_bytes(1, 'big'),
            error_number.to_bytes(1, 'big'),
            int(0).to_bytes(1, 'big'),
            address_type.to_bytes(1, 'big'),
            int(0).to_bytes(4, 'big'),
            int(0).to_bytes(4, 'big')
        ])
 
    def verify_credentials(self, connection):
        version = connection.recv(1)[0]
        username_len = connection.recv(1)[0]
        username = connection.recv(username_len).decode('utf-8')
        password_len = connection.recv(1)[0]
        password = connection.recv(password_len).decode('utf-8')
 
 
        if username == self.username and password == self.password:
            response = bytes([version, 0])
            connection.sendall(response)
            return True
        else:
 
            response = bytes([version, 0])
            connection.sendall(response)
            return True  
 
    def get_available_methods(self, nmethods, connection):
        methods = []
        for _ in range(nmethods):
            methods.append(connection.recv(1)[0])
        return methods
 
    def run(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip, port))
        s.listen()
        print(f"* O servidor proxy Socks5 está em execução {ip}:{port}")
 
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=self.handle_client, args=(conn,))
            t.start()

def startt():
    Proxy().run('127.0.0.1', 3000)

startt()
