from app.components.base_list_frame import BaseListFrame
from app.services.semestre_services import SemestreService

class SemestresFrame(BaseListFrame):
    def get_items(self,conexao):
        return self.service.semestre_service.listar()

    def modal_class_add(self):
        from app.components.modal_novo_semestre import ModalNovoSemestre
        return ModalNovoSemestre
    
    def modal_class_update(self):
        from app.components.modal_atualiza_semestre import ModalAtualizaSemestre
        return ModalAtualizaSemestre

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
        return self.service.semestre_service.deletar(item)
    
    def update_item(self, item):
        print("Atualizando semestre")
        return "Atualizar Semestre"
