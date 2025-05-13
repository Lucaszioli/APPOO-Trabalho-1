from app.components.base_list_frame import BaseListFrame
from app.services.semestre_services import SemestreService
from app.components.modal_novo_semestre import ModalNovoSemestre

class SemestresFrame(BaseListFrame):
    def get_items(self, conexao):
        return SemestreService.listar_semestres(conexao)

    def modal_class(self):
        return ModalNovoSemestre

    def detail_view_class(self):
        from app.views.pagina_semestre import PaginaSemestre
        return PaginaSemestre

    def get_id(self, semestre):
        return semestre.id

    def item_name(self, semestre):
        return semestre.nome

    def item_name_singular(self):
        return "semestre"

    def item_name_plural(self):
        return "semestres"

    def title_text(self):
        return "Seja Bem-Vindo(a)"

    def subtitle_text(self):
        return "Selecione um semestre:"

    def add_button_text(self):
        return "Adicionar Semestre"
    
    def delete_item(self, item):
        return SemestreService.deletar_bd(item, self.conexao)
    
    def update_item(self, item):
        return "Atualizar Semestre"
