from conexion.conexao import criar_tabelas
from controller.curso_controller import inserir_curso, listar_cursos
from controller.estudante_controller import inserir_estudante, listar_estudantes
from controller.nota_controller import registrar_nota
from reports.relatorio_media_turma import media_por_turma
from reports.relatorio_desempenho_curso import desempenho_por_curso
from model.curso import Curso
from model.estudante import Estudante
from model.nota import Nota

def main():
    criar_tabelas()

    print("==== SISTEMA DE CONTROLE DE ESTUDANTES ====")
    while True:
        print("\n1 - Cadastrar Curso")
        print("2 - Cadastrar Estudante")
        print("3 - Registrar Nota")
        print("4 - Relatório: Média por Turma")
        print("5 - Relatório: Desempenho por Curso")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome do curso: ")
            carga = int(input("Carga horária: "))
            inserir_curso(Curso(nome=nome, carga_horaria=carga))
            print("Curso cadastrado!")
        elif opcao == "2":
            nome = input("Nome do estudante: ")
            matricula = input("Matrícula: ")
            listar = listar_cursos()
            for c in listar:
                print(f"{c[0]} - {c[1]}")
            curso_id = int(input("ID do curso: "))
            inserir_estudante(Estudante(nome=nome, matricula=matricula, curso_id=curso_id))
            print("Estudante cadastrado!")
        elif opcao == "3":
            listar = listar_estudantes()
            for e in listar:
                print(f"{e[0]} - {e[1]} ({e[3]})")
            estudante_id = int(input("ID do estudante: "))
            disciplina = input("Disciplina: ")
            nota = float(input("Nota: "))
            registrar_nota(Nota(estudante_id=estudante_id, disciplina=disciplina, nota=nota))
            print("Nota registrada!")
        elif opcao == "4":
            for curso, media in media_por_turma():
                print(f"{curso}: média {media:.2f}")
        elif opcao == "5":
            for curso, estudante, media in desempenho_por_curso():
                print(f"{curso} - {estudante}: média {media:.2f}")
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
