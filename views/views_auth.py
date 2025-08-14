from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils import timezone
from account_tools.utils.utils import validar_email, gerar_codigo, gerar_hash_codigo

def cadastrar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'cadastro.html', {'erro': 'Username e senha são obrigatórios'})

        if not validar_email(email):
            return render(request, 'cadastro.html', {'erro': 'Formato de e-mail inválido'})

        if len(password) < 6:
            return render(request, 'cadastro.html', {'erro': 'A senha deve ter pelo menos 6 caracteres'})

        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro.html', {'erro': 'Esse usuário já existe'})

        if User.objects.filter(email=email).exists():
            return render(request, 'cadastro.html', {'erro': 'Esse e-mail já existe'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        codigo = gerar_codigo()
        codigo_hash = gerar_hash_codigo(codigo)

        try:
            send_mail(
                'Código de Confirmação',
                f'Seu código de verificação é: {codigo}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            user.delete()
            return render(request, 'cadastro.html', {'erro': f'Erro ao enviar e-mail: {str(e)}'})

        request.session['codigo_confirmacao'] = codigo_hash
        request.session['usuario_cadastrado_id'] = user.id
        request.session['codigo_hora'] = timezone.now().timestamp()
        request.session['email'] = email

        return render(request, 'confirmar_cadastro.html', {'email': email})

    return render(request, 'cadastro.html')


def montar_contexto(request, erro_msg=None, sucesso_msg=None, email=None):
    codigo_hora = request.session.get('codigo_hora')
    tentativas = request.session.get('tentativas_confirmacao', 0)
    tempo_restante = max(0, 600 - (timezone.now().timestamp() - codigo_hora)) if codigo_hora else 0

    minutos = int(tempo_restante // 60)
    segundos = int(tempo_restante % 60)

    return {
        'erro': erro_msg,
        'mensagem': sucesso_msg,
        'tempo_restante': int(tempo_restante),
        'tempo_expirado': tempo_restante <= 0,
        'tempo_formatado': f"{minutos:02d}:{segundos:02d}",
        'tentativas': tentativas,
        'email': email or request.session.get('email'),
    }


def confirmar_codigo(request):
    usuario_id = request.session.get('usuario_cadastrado_id')
    email = None
    if usuario_id:
        user = User.objects.filter(id=usuario_id).first()
        if user:
            email = user.email

    if request.method == 'POST':
        codigo_digitado = request.POST.get('codigo')
        codigo_hash_esperado = request.session.get('codigo_confirmacao')
        codigo_hora = request.session.get('codigo_hora')
        tentativas = request.session.get('tentativas_confirmacao', 0)

        if not codigo_hash_esperado or not usuario_id or not codigo_hora:
            return render(request, 'confirmar_cadastro.html', montar_contexto(request, 'Sessão expirada. Tente novamente.', email=email))

        agora = timezone.now().timestamp()
        if agora - codigo_hora > 600:
            limpar_sessao_confirmacao(request)
            return render(request, 'confirmar_cadastro.html', montar_contexto(request, 'Código expirado. Solicite um novo cadastro.', email=email))

        if tentativas >= 3:
            return render(request, 'confirmar_cadastro.html', montar_contexto(request, 'Número máximo de tentativas excedido. Reenvie o código.', email=email))

        if gerar_hash_codigo(codigo_digitado) == codigo_hash_esperado:
            user = User.objects.get(id=usuario_id)
            user.is_active = True
            user.save()
            limpar_sessao_confirmacao(request)
            return render(request, 'confirmar_cadastro.html', montar_contexto(request, sucesso_msg='Cadastro confirmado com sucesso!', email=email))

        request.session['tentativas_confirmacao'] = tentativas + 1
        return render(request, 'confirmar_cadastro.html', montar_contexto(request, f'Código incorreto. Tentativa {tentativas + 1} de 3.', email=email))

    return render(request, 'confirmar_cadastro.html', montar_contexto(request, email=email))


def reenviar_codigo(request):
    usuario_id = request.session.get('usuario_cadastrado_id')
    if not usuario_id:
        return redirect('cadastrar_usuario')

    agora = timezone.now().timestamp()
    ultimo_envio = request.session.get('ultimo_envio_codigo', 0)

    if agora - ultimo_envio < 60:
        wait = int(60 - (agora - ultimo_envio))
        return render(request, 'confirmar_cadastro.html', montar_contexto(request, f'Aguarde {wait} segundos para reenviar o código.'))

    user = User.objects.get(id=usuario_id)
    codigo = gerar_codigo()
    codigo_hash = gerar_hash_codigo(codigo)

    try:
        send_mail(
            'Código de Confirmação - Reenvio',
            f'Seu código de verificação é: {codigo}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        return render(request, 'confirmar_cadastro.html', montar_contexto(request, f'Erro ao enviar e-mail: {e}', email=user.email))

    request.session['codigo_confirmacao'] = codigo_hash
    request.session['codigo_hora'] = agora
    request.session['ultimo_envio_codigo'] = agora
    request.session['tentativas_confirmacao'] = 0

    return render(request, 'confirmar_cadastro.html', montar_contexto(request, 'Código reenviado com sucesso!', email=user.email))


def limpar_sessao_confirmacao(request):
    for chave in ['codigo_confirmacao', 'codigo_hora', 'usuario_cadastrado_id', 'tentativas_confirmacao', 'ultimo_envio_codigo', 'email']:
        request.session.pop(chave, None)