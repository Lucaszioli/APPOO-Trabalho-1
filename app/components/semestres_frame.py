from typing import Any
from datetime import datetime
from app.components.improved_list_frame import ImprovedListFrame, ItemCard
from app.components.ui.base_components import StyledLabel
import customtkinter

class SemestreCard(ItemCard):
    """Card específico para semestres."""
    
    def _add_item_info(self, parent):
        """Adiciona informações específicas do semestre."""
        info_container = customtkinter.CTkFrame(parent, fg_color="transparent")
        info_container.pack(fill="x")
        info_container.grid_columnconfigure((0, 1), weight=1)
        
        # Data de início
        inicio_text = self._format_date(self.item.data_inicio)
        inicio_label = StyledLabel(
            info_container,
            text=f"Início: {inicio_text}",
            style='small'
        )
        inicio_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        # Data de fim
        fim_text = self._format_date(self.item.data_fim)
        fim_label = StyledLabel(
            info_container,
            text=f"Fim: {fim_text}",
            style='small'
        )
        fim_label.grid(row=0, column=1, sticky="e")
        
        # Status (ativo/inativo)
        status_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        status_frame.pack(fill="x", pady=(5, 0))
        
        status_text, status_color = self._get_status_info()
        status_label = StyledLabel(
            status_frame,
            text=status_text,
            style='small',
            text_color=status_color
        )
        status_label.pack(anchor="w")
        
        # Número de disciplinas (se disponível)
        if hasattr(self.item, 'disciplinas_count'):
            count_label = StyledLabel(
                status_frame,
                text=f"{self.item.disciplinas_count} disciplinas",
                style='caption'
            )
            count_label.pack(anchor="w", pady=(2, 0))
    
    def _format_date(self, date_obj):
        """Formata data para exibição."""
        if isinstance(date_obj, str):
            try:
                date_obj = datetime.strptime(date_obj, "%Y-%m-%d")
            except ValueError:
                return date_obj
        
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%d/%m/%Y")
        
        return str(date_obj)
    
    def _get_status_info(self):
        """Retorna informações de status do semestre."""
        try:
            hoje = datetime.now().date()
            if isinstance(self.item.data_inicio, str):
                inicio = datetime.strptime(self.item.data_inicio, "%d/%m/%Y").date()
            else:
                inicio = self.item.data_inicio
                print(inicio)
                
            if isinstance(self.item.data_fim, str):
                fim = datetime.strptime(self.item.data_fim, "%d/%m/%Y").date()
            else:
                fim = self.item.data_fim
            
            if hoje < inicio:
                return "Futuro", ("blue", "#1f538d")
            elif hoje > fim:
                return "Concluído", ("gray50", "gray60")
            else:
                return "Ativo", ("green", "#28a745")
                
        except Exception:
            return "Indefinido", ("gray40", "gray50")

class SemestresFrame(ImprovedListFrame):
    """Frame para listar e gerenciar semestres com design melhorado."""

    def get_items(self, conexao: Any):
        """Retorna todos os semestres cadastrados e carrega suas disciplinas."""
        semestres = self.service.semestre_service.listar()
        for semestre in semestres:
            self.service.semestre_service.carregar_disciplinas(semestre)
        return semestres

    def modal_class_add(self):
        """Classe do modal usado para criar novo semestre."""
        from app.components.modal_novo_semestre import ModalNovoSemestre
        return ModalNovoSemestre
    
    def modal_class_update(self):
        """Classe do modal usado para atualizar semestre."""
        from app.components.modal_atualiza_semestre import ModalAtualizaSemestre
        return ModalAtualizaSemestre

    def detail_view_class(self):
        """Classe da view de detalhe de semestre."""
        from app.views.pagina_semestre import PaginaSemestre
        return PaginaSemestre

    def get_id(self, item: Any):
        """Extrai o identificador único do semestre."""
        return getattr(item, "id", None)

    def item_name(self, item: Any):
        """Extrai o nome do semestre para exibição."""
        return getattr(item, "nome", "")

    def item_name_singular(self):
        return "semestre"

    def item_name_plural(self):
        return "semestres"

    def title_text(self):
        return "Sistema de Gerenciamento Acadêmico"

    def subtitle_text(self):
        return "Selecione um semestre para gerenciar suas disciplinas"

    def add_button_text(self):
        return "Novo Semestre"

    def delete_item(self, item):
        """Deleta um semestre."""
        return self.service.semestre_service.deletar(item)

    def update_item(self, item):
        """Atualiza um semestre."""
        pass
        
    def _create_item_card(self, item):
        """Cria card customizado para semestre."""
        return SemestreCard(self.list_container, item, self)
        
    def _get_stats_text(self):
        """Retorna estatísticas específicas dos semestres."""
        total = len(self.items)
        ativos = sum(1 for item in self.items if self._is_semestre_ativo(item))
        return f"Total: {total} semestres • {ativos} ativos"
        
    def _is_semestre_ativo(self, semestre):
        """Verifica se um semestre está ativo."""
        try:
            hoje = datetime.now().date()
            
            if isinstance(semestre.data_inicio, str):
                inicio = datetime.strptime(semestre.data_inicio, "%Y-%m-%d").date()
            else:
                inicio = semestre.data_inicio
                
            if isinstance(semestre.data_fim, str):
                fim = datetime.strptime(semestre.data_fim, "%Y-%m-%d").date()
            else:
                fim = semestre.data_fim
            
            return inicio <= hoje <= fim
        except Exception:
            return False
