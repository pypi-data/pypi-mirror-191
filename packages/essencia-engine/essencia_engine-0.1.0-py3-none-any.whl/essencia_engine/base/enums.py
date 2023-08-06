__all__ = [
    'BaseEnum',
    'PaymentMethod',
    'ProfileType',
    'ExpenseType',
    'Gender',
    'VisitType',
    'ServiceType',
    'ProviderType',
    'BankAccount',
    'DepositMethod',
    'CostType'
]

from enum import Enum


class BaseEnum(Enum):

    @classmethod
    def label(cls):
        return cls.__name__

    @classmethod
    def is_enum(cls):
        return True

    @classmethod
    def options(cls):
        return {item.name: item.value for item in cls.__members__.values()}

    @classmethod
    async def select_options(cls):
        text = f'<option></option>\n'
        for name, item in cls.__members__.items():
            text += f'<option value="{name}">{item.value}</option>\n'
        return text


class VisitType(BaseEnum):
    INITIAL = 'Inicial'
    REVISION = 'Revisão'
    FOLLOWUP = 'Seguimento'
    RETURN = 'Retorno'

    @classmethod
    def label(cls):
        return 'Tipo de Visita'


class Gender(BaseEnum):
    M = 'Masculino'
    F = 'Feminino'

    @classmethod
    def label(cls):
        return 'Gênero (ao nascer)'


class CostType(BaseEnum):
    PRO01 = 'Pro Labore'

    CLT00 = 'CLT FGTS'
    CLT01 = 'CLT Salário'
    CLT02 = 'CLT Férias'
    CLT03 = 'CLT Décimo Terceiro'
    CLT04 = 'CLT Admissional'
    CLT05 = 'CLT Demissional'
    CLT06 = 'CLT INSS'

    ADI01 = 'Adicional Transporte'
    ADI02 = 'Adicional Assiduidade'
    ADI03 = 'Adicional Insalubridade'
    ADI04 = 'Adicional Quinquênio'
    ADI05 = 'Adicional Administrativo'
    ADI06 = 'Adicional Suporte Clínico'

    EMP01 = 'Contratado Terceirizado'
    EMP02 = 'Contratado Diarista'

    IMP01 = 'Imposto Simples'
    IMP02 = 'Imposto Federal'
    IMP03 = 'Imposto Estadual'
    IMP04 = 'Imposto Municipal'

    CON01 = 'Conta de Luz'
    CON02 = 'Conta de Água'
    CON03 = 'Conta de Telefone e Internet'

    AUT01 = 'CRM Médico'
    AUT02 = 'CRM Empresa'
    AUT03 = 'Vigilância Sanitária'
    AUT04 = 'Bombeiros'

    COS03 = 'Compra Supermercado'
    COS04 = 'Compra Farmácia'
    COS07 = 'Compra Papelaria'
    COS08 = 'Compra Material de Limpeza'
    COS15 = 'Compra de Equipamento de Segurança'
    COS01 = 'Compra não Listada'

    COS09 = 'Serviço Avulso de Eletricista'
    COS10 = 'Serviço Avulso de Pedreito'
    COS11 = 'Serviço Avulso de Pintor'
    COS12 = 'Serviço Avulso de Marcineiro'
    COS13 = 'Serviço Avulso de Segurança'
    COS14 = 'Serviço Avulso de Limpeza'
    COS02 = 'Serviço Avulso não Listado'

    COS05 = 'Plano de Saúde'
    COS06 = 'Taxa Bancária'
    COS00 = 'Custo não Listado'

    @classmethod
    def duty(cls):
        return [cls.IMP01, cls.IMP02, cls.IMP03, cls.IMP04]

    @classmethod
    def clt(cls):
        return [cls.CLT00, cls.CLT01, cls.CLT02, cls.CLT03, cls.CLT04, cls.CLT04]

    @classmethod
    def employee(cls):
        return [
            cls.CLT01, cls.CLT02, cls.CLT03, cls.CLT04, cls.CLT04,
            cls.ADI01, cls.ADI02, cls.ADI03, cls.ADI04, cls.ADI05, cls.ADI06,
            cls.EMP01, cls.EMP02,
            cls.PRO01
        ]


class ExpenseType(BaseEnum):
    SAL = 'Salário'
    FER = 'Férias'
    DEC = 'Décimo Terceiro'
    FGT = 'FGTS'
    ACE = 'Acerto Demissional'
    LUZ = 'Luz'
    AGU = 'Água'
    LIM = 'Limpeza'
    SER = 'Serviço Terceirizado'
    COM = 'Compra'
    IMP = 'Imposto'
    EST = 'Estágio'
    OUT = 'Outro'

    @classmethod
    def label(cls):
        return 'Tipo de Despesa'


class ProfileType(BaseEnum):
    PA = 'Patient'
    MD = 'Doctor'
    NU = 'Assistant'
    TH = 'Therapist'
    EM = 'Employee'
    FE = 'Fellow'
    CO = 'Colaborator'
    SU = 'Supplier'

    @classmethod
    def label(cls):
        return 'Tipo de Perfil'


class ProviderType(BaseEnum):
    MD = 'Médico'
    TH = 'Terapeuta'

    @classmethod
    def label(cls):
        return 'Tipo de Profissional'


class PaymentMethod(BaseEnum):
    CA = 'Dinheiro'
    CR = 'Crédito'
    DE = 'Débito'
    TR = 'Transferência bancária'
    CH = 'Cheque'
    PI = 'PIX'

    @classmethod
    def label(cls):
        return 'Método de Pagamento'


class ServiceType(BaseEnum):
    CO = 'Consulta Regular'
    CI = 'Consulta Inicial'
    CE = 'Consulta de Encaixe'
    CC = 'Consulta Cortesia'
    CP = 'Consulta Breve'
    VH = 'Visita Hospitalar'
    VD = 'Visita Domiciliar'
    RT = 'Retorno de Consulta'
    SE = 'Sessão de Terapia'
    SA = 'Sessão de Terapia Assistida'
    SG = 'Sessão em Grupo'
    AL = 'Aluguel de Sala'
    AC = 'Aluguel de Diárias'
    SU = 'Suporte de Logística'
    VE = 'Venda de Produto'
    OS = 'Outro Serviço'
    AD = 'Acerto de débito'


    @classmethod
    def rent(cls):
        return [cls.AL, cls.AC]

    @classmethod
    def medical_service(cls):
        return [cls.CO, cls.RT, cls.CI, cls.CE, cls.CC, cls.VD, cls.VH, cls.CP]

    @classmethod
    def facility_service(cls):
        return [cls.VE, cls.SU, *cls.rent(), cls.OS]

    @classmethod
    def therapy_session(cls):
        return [cls.SE, cls.SA, cls.SG]

    @classmethod
    def debit_payment(cls):
        return [cls.AD]


    @classmethod
    def payment(cls):
        return [*cls.rent(), *cls.debit_payment()]


class BankAccount(BaseEnum):
    DBR = 'Bradesco'
    DCA = 'Caixa'
    EBB = 'Banco do Brasil'
    EIT = 'Itaú'


class DepositMethod(BaseEnum):
    DI = 'Dinheiro'
    CH = 'Cheque'
    DC = 'Dinheiro e Cheque'
    TR = 'Transferência Bancária'
    PI = 'Pix'
