from src import crud
from src.crud import listar_estudantes, listar_cursos, listar_notas
import sys

def pause():
    input('\nPressione Enter para continuar...')

def menu_principal():
    while True:
        print('\n=== CONTROLE DE ESTUDANTES, CURSOS E NOTAS ===')
        print('1. Estudantes')
        print('2. Cursos')
        print('3. Notas')
        print('4. Relatórios')
        print('0. Sair')
        op = input('> ')
        if op == '1':
            menu_estudantes()
        elif op == '2':
            menu_cursos()
        elif op == '3':
            menu_notas()
        elif op == '4':
            menu_relatorios()
        elif op == '0':
            print('Saindo...'); sys.exit(0)
        else:
            print('Opção inválida.')

def menu_estudantes():
    while True:
        print('\n--- Estudantes ---')
        print('1. Listar estudantes')
        print('2. Cadastrar estudante')
        print('3. Atualizar estudante')
        print('4. Excluir estudante')
        print('0. Voltar')
        op = input('> ')
        if op == '1':
            studs = listar_estudantes()
            for s in studs:
                print(f'ID: {s.id} | Nome: {s.nome} | Matrícula: {s.matricula} | Email: {s.email}')
            pause()
        elif op == '2':
            nome = input('Nome: '); mat = input('Matrícula: '); email = input('Email: ')
            crud.criar_estudante(nome, mat, email)
            print('Estudante criado.'); pause()
        elif op == '3':
            idd = input('ID do estudante: '); nome = input('Novo nome (enter p/ manter): ')
            nome = None if nome.strip()=='' else nome
            mat = input('Nova matrícula (enter p/ manter): '); mat = None if mat.strip()=='' else mat
            email = input('Novo email (enter p/ manter): '); email = None if email.strip()=='' else email
            crud.atualizar_estudante(int(idd), nome, mat, email)
            print('Atualizado.'); pause()
        elif op == '4':
            idd = input('ID do estudante a excluir: ')
            crud.excluir_estudante(int(idd)); print('Excluído.'); pause()
        elif op == '0': break
        else: print('Opção inválida.')

def menu_cursos():
    while True:
        print('\n--- Cursos ---')
        print('1. Listar cursos')
        print('2. Cadastrar curso')
        print('3. Atualizar curso')
        print('4. Excluir curso')
        print('0. Voltar')
        op = input('> ')
        if op == '1':
            cursos = listar_cursos()
            for c in cursos:
                print(f'ID: {c.id} | Nome: {c.nome} | Carga: {c.carga_horaria}h')
            pause()
        elif op == '2':
            nome = input('Nome do curso: '); ch = input('Carga horária: ')
            chn = int(ch) if ch.strip()!='' else None
            crud.criar_curso(nome, chn); print('Curso criado.'); pause()
        elif op == '3':
            idd = input('ID do curso: '); nome = input('Novo nome (enter p/ manter): ')
            nome = None if nome.strip()=='' else nome
            ch = input('Nova carga (enter p/ manter): '); chn = None if ch.strip()=='' else int(ch)
            crud.atualizar_curso(int(idd), nome, chn); print('Atualizado.'); pause()
        elif op == '4':
            idd = input('ID do curso a excluir: '); crud.excluir_curso(int(idd)); print('Excluído.'); pause()
        elif op == '0': break
        else: print('Opção inválida.')

def menu_notas():
    while True:
        print('\n--- Notas ---')
        print('1. Listar notas')
        print('2. Lançar nota')
        print('3. Atualizar nota')
        print('4. Excluir nota')
        print('0. Voltar')
        op = input('> ')
        if op == '1':
            rows = listar_notas()
            for r in rows:
                print(f'ID_NOTA: {r[0]} | Estudante: ({r[1]}) {r[2]} | Curso: ({r[3]}) {r[4]} | N1: {r[5]} | N2: {r[6]} | MÉDIA: {r[7]}')
            pause()
        elif op == '2':
            ide = int(input('ID do estudante: ')); idc = int(input('ID do curso: '))
            n1 = input('Nota 1 (enter p/ none): '); n2 = input('Nota 2 (enter p/ none): ')
            n1v = None if n1.strip()=='' else float(n1); n2v = None if n2.strip()=='' else float(n2)
            crud.lancar_nota(ide, idc, n1v, n2v); print('Nota lançada.'); pause()
        elif op == '3':
            idn = int(input('ID da nota: '))
            n1 = input('Nova nota 1 (enter p/ manter): '); n1v = None if n1.strip()=='' else float(n1)
            n2 = input('Nova nota 2 (enter p/ manter): '); n2v = None if n2.strip()=='' else float(n2)
            ok = crud.atualizar_nota(idn, n1v, n2v)
            print('Atualizado.' if ok else 'Nota não encontrada.'); pause()
        elif op == '4':
            idn = int(input('ID da nota: ')); crud.excluir_nota(idn); print('Excluído.'); pause()
        elif op == '0': break
        else: print('Opção inválida.')

def menu_relatorios():
    while True:
        print('\n--- Relatórios ---')
        print('1. Relatório por estudante')
        print('2. Média por curso')
        print('0. Voltar')
        op = input('> ')
        if op == '1':
            ide = int(input('ID do estudante: '))
            rows = crud.relatorio_desempenho_por_estudante(ide)
            for r in rows:
                print(f'Curso: {r[0]} | N1: {r[1]} | N2: {r[2]} | Média: {r[3]} | Situação: {r[4]}')
            pause()
        elif op == '2':
            idc = int(input('ID do curso: '))
            m = crud.relatorio_media_por_curso(idc)
            print(f'Média do curso: {m}')
            pause()
        elif op == '0': break
        else: print('Opção inválida.')

if __name__ == '__main__':
    menu_principal()
