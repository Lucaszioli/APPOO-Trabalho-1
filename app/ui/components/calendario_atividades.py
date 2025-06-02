import customtkinter
from datetime import datetime, timedelta
from typing import List, Any, Optional
from app.ui.components.components_base import BaseComponent, StyledLabel, Card, StyledButton
import calendar

class AtividadeItem(customtkinter.CTkFrame):
    """Widget para exibir uma atividade individual no calendário."""
    
    def __init__(self, master, atividade: Any, disciplina_nome: str, **kwargs):
        super().__init__(master, **kwargs)
        self.atividade = atividade
        self.disciplina_nome = disciplina_nome
        self._setup_ui()
        
    def _setup_ui(self):
        """Configura a interface do item de atividade."""
        tipo_cores = {
            "Trabalho": ("red", "darkred"),
            "Prova": ("orange", "darkorange"), 
            "Aula de campo": ("green", "darkgreen"),
            "Aula de revisão": ("blue", "darkblue")
        }
        
        tipo = getattr(self.atividade, 'tipo', 'Outro')
        cor_normal, cor_hover = tipo_cores.get(tipo, ("gray", "darkgray"))
        
        self.configure(
            fg_color=cor_normal,
            corner_radius=8,
            height=60
        )
        
        content_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=8, pady=6)
        
        nome_label = StyledLabel(
            content_frame,
            text=self.atividade.nome,
            style='small',
            text_color="white"
        )
        nome_label.pack(anchor="w")
        
        data_str = self.atividade.data
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y")
            data_formatada = data_obj.strftime("%d/%m")
        except:
            data_formatada = data_str
            
        info_label = StyledLabel(
            content_frame,
            text=f"{data_formatada} • {self.disciplina_nome}",
            style='caption',
            text_color="white"
        )
        info_label.pack(anchor="w")
        
        if hasattr(self.atividade, 'progresso'):
            progresso_label = StyledLabel(
                content_frame,
                text=f"Status: {self.atividade.progresso}",
                style='caption',
                text_color="white"
            )
            progresso_label.pack(anchor="w")

class CalendarioAtividades(BaseComponent):
    """Componente de calendário que mostra as próximas atividades."""
    
    def __init__(self, master, service, disciplina=None, semestre=None, **kwargs):
        self.service = service
        self.disciplina = disciplina
        self.semestre = semestre
        self.current_period = "proximos_7_dias"  
        super().__init__(master, **kwargs)
        
    def _setup_style(self):
        super()._setup_style()
        self.configure(fg_color="transparent")
        
    def _build_ui(self):
        """Constrói a interface do calendário."""
        
        header_card = Card(self, title="Próximas Atividades")
        header_card.pack(fill="x", padx=10, pady=(0, 10))
        
        self._create_period_filters(header_card.content_frame)
        
        self.atividades_container = customtkinter.CTkScrollableFrame(
            self,
            height=400,
            fg_color=("gray95", "gray15")
        )
        self.atividades_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.current_period = "proximos_7_dias"
        self._load_atividades()
        
    def _create_period_filters(self, parent):
        """Cria os filtros de período."""
        filter_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(10, 0))
        
        periods = [
            ("proximos_7_dias", "Próximos 7 dias"),
            ("proximos_15_dias", "Próximos 15 dias"),
            ("este_mes", "Este mês"),
            ("proximo_mes", "Próximo mês")
        ]
        
        for i, (period_key, period_label) in enumerate(periods):
            btn = StyledButton(
                filter_frame,
                text=period_label,
                style='secondary' if period_key != self.current_period else 'primary',
                command=lambda p=period_key: self._change_period(p),
                width=120,
                height=32
            )
            btn.grid(row=0, column=i, padx=(0, 5), sticky="w")
            
        filter_frame.grid_columnconfigure(4, weight=1)
        
    def _change_period(self, period_key):
        """Muda o período de visualização."""
        if self.current_period == period_key:
            return
            
        self.current_period = period_key
        self._update_filter_buttons()
        self._load_atividades()
        
    def _update_filter_buttons(self):
        """Atualiza o estilo dos botões de filtro."""
        for widget in self.children.values():
            if isinstance(widget, Card):
                for child in widget.content_frame.winfo_children():
                    if isinstance(child, customtkinter.CTkFrame):
                        child.destroy()
                        self._create_period_filters(widget.content_frame)
                        break
                break
                
    def _load_atividades(self):
        """Carrega as atividades baseado no período selecionado."""
        for widget in self.atividades_container.winfo_children():
            widget.destroy()
            
        try:
            print(f"Carregando atividades para período: {self.current_period}")
            atividades = self._get_atividades_for_period()
            print(f"Encontradas {len(atividades)} atividades")
            
            atividades_com_disciplina = self._enrich_atividades_with_disciplina(atividades)
            
            if not atividades_com_disciplina:
                self._show_empty_message()
                return
                
            atividades_por_data = self._group_by_date(atividades_com_disciplina)
            
            for data, atividades_data in atividades_por_data.items():
                self._create_date_section(data, atividades_data)
                
        except Exception as e:
            print(f"Erro detalhado: {e}")
            import traceback
            traceback.print_exc()
            error_label = StyledLabel(
                self.atividades_container,
                text=f"Erro ao carregar atividades: {str(e)}",
                style='small'
            )
            error_label.pack(pady=20)
            
    def _get_atividades_for_period(self) -> List[Any]:
        """Obtém as atividades para o período selecionado."""
        hoje = datetime.now().date()
        print(f"Data de hoje: {hoje}")
        
        if self.current_period == "proximos_7_dias":
            fim = hoje + timedelta(days=7)
        elif self.current_period == "proximos_15_dias":
            fim = hoje + timedelta(days=15)
        elif self.current_period == "este_mes":
            fim = hoje.replace(day=calendar.monthrange(hoje.year, hoje.month)[1])
        elif self.current_period == "proximo_mes":
            if hoje.month == 12:
                fim = hoje.replace(year=hoje.year + 1, month=1, day=calendar.monthrange(hoje.year + 1, 1)[1])
            else:
                fim = hoje.replace(month=hoje.month + 1, day=calendar.monthrange(hoje.year, hoje.month + 1)[1])
        else:
            fim = hoje + timedelta(days=7)
        
        print(f"Período: {hoje} até {fim}")
            
        if self.disciplina:
            print("Buscando atividades por disciplina")
            atividades = self.service.atividade_service.listar_por_disciplina(self.disciplina)
        elif self.semestre:
            print(f"Buscando atividades por semestre: {self.semestre.nome}")
            atividades = self.service.atividade_service.listar_por_semestre(self.semestre)
        else:
            print("Buscando todas as atividades")
            atividades = self.service.atividade_service.listar()
        
        print(f"Atividades encontradas: {len(atividades)}")
            
        atividades_filtradas = []
        for i, atividade in enumerate(atividades):
            try:
                print(f"Processando atividade {i}: {atividade.nome}, data: {atividade.data}")
                
                if not hasattr(atividade, 'data') or not atividade.data:
                    print(f"Atividade {i} não tem data válida")
                    continue
                    
                data_atividade = datetime.strptime(atividade.data, "%d/%m/%Y").date()
                print(f"Data convertida: {data_atividade}")
                
                if hoje <= data_atividade <= fim:
                    atividades_filtradas.append(atividade)
                    print(f"Atividade {i} incluída no período")
                else:
                    print(f"Atividade {i} fora do período")
                    
            except (ValueError, TypeError, AttributeError) as e:
                print(f"Erro ao processar atividade {i}: {e}")
                continue
                
        try:
            atividades_filtradas.sort(key=lambda a: datetime.strptime(a.data, "%d/%m/%Y") if a.data else datetime.min)
        except (ValueError, TypeError, AttributeError):
            pass
        return atividades_filtradas
        
    def _enrich_atividades_with_disciplina(self, atividades: List[Any]) -> List[tuple]:
        """Enriquece as atividades com informações da disciplina."""
        resultado = []
        for atividade in atividades:
            try:
                if not hasattr(atividade, 'disciplina_id') or atividade.disciplina_id is None:
                    resultado.append((atividade, "Disciplina não definida"))
                    continue
                    
                disciplina = self.service.disciplina_service.buscar_por_id(atividade.disciplina_id)
                if disciplina and hasattr(disciplina, 'nome'):
                    resultado.append((atividade, disciplina.nome))
                else:
                    resultado.append((atividade, "Disciplina não encontrada"))
            except Exception as e:
                resultado.append((atividade, f"Erro ao carregar disciplina: {str(e)}"))
        return resultado
        
    def _group_by_date(self, atividades_com_disciplina: List[tuple]) -> dict:
        """Agrupa atividades por data."""
        grupos = {}
        for atividade, disciplina_nome in atividades_com_disciplina:
            try:
                data = getattr(atividade, 'data', None)
                if not data:
                    continue
                    
                if data not in grupos:
                    grupos[data] = []
                grupos[data].append((atividade, disciplina_nome))
            except Exception:
                continue
        return grupos
        
    def _create_date_section(self, data: str, atividades_data: List[tuple]):
        """Cria uma seção para uma data específica."""
        try:
            data_obj = datetime.strptime(data, "%d/%m/%Y")
            data_formatada = data_obj.strftime("%d/%m/%Y (%A)")
            
            hoje = datetime.now().date()
            if data_obj.date() == hoje:
                data_formatada += " - HOJE"
            elif data_obj.date() == hoje + timedelta(days=1):
                data_formatada += " - AMANHÃ"
        except:
            data_formatada = data
            
        date_card = Card(self.atividades_container, title=data_formatada)
        date_card.pack(fill="x", pady=(0, 10))
        
        for atividade, disciplina_nome in atividades_data:
            atividade_item = AtividadeItem(
                date_card.content_frame,
                atividade,
                disciplina_nome,
                height=70
            )
            atividade_item.pack(fill="x", pady=(0, 5))
            
    def _show_empty_message(self):
        """Mostra mensagem quando não há atividades."""
        empty_card = Card(self.atividades_container, title="Nenhuma atividade encontrada")
        empty_card.pack(fill="x", pady=20)
        
        message_label = StyledLabel(
            empty_card.content_frame,
            text="Não há atividades programadas para este período.",
            style='normal'
        )
        message_label.pack(pady=10)
        
    def refresh(self):
        """Atualiza o calendário."""
        self._load_atividades()
        
    def set_disciplina(self, disciplina):
        """Define a disciplina para filtrar atividades."""
        self.disciplina = disciplina
        self.semestre = None
        self.refresh()
        
    def set_semestre(self, semestre):
        """Define o semestre para filtrar atividades."""
        self.semestre = semestre
        self.disciplina = None
        self.refresh()
