from starlette.endpoints import HTTPEndpoint
from functools import reduce

from essencia_engine.base.types import *
from essencia_engine.base.function import *
from essencia_engine.base.enums import *
from essencia_engine.base.ntuple import *
from essencia_engine.base.session import *
from essencia_engine.base.context import *
from essencia_engine.base.setup import templates, static
from essencia_engine.base.endpoint import BaseEndpoint
from essencia_engine import models



class PersonEndpoint(BaseEndpoint):
	MODEL = models.Person


class PatientEndpoint(BaseEndpoint):
	MODEL = models.Patient
	INITIAL_ROUTES = PersonEndpoint.routes()


class DoctorEndpoint(BaseEndpoint):
	MODEL = models.Doctor
	INITIAL_ROUTES = PatientEndpoint.routes()


class AssistantEndpoint(BaseEndpoint):
	MODEL = models.Assistant
	INITIAL_ROUTES = DoctorEndpoint.routes()


class TherapistEndpoint(BaseEndpoint):
	MODEL = models.Therapist
	INITIAL_ROUTES = AssistantEndpoint.routes()


class EmployeeEndpoint(BaseEndpoint):
	MODEL = models.Employee
	INITIAL_ROUTES = TherapistEndpoint.routes()


class UserEndpoint(BaseEndpoint):
	MODEL = models.User
	INITIAL_ROUTES = EmployeeEndpoint.routes()


class UserProfileRelationEndpoint(BaseEndpoint):
	MODEL = models.UserProfileRelation
	INITIAL_ROUTES = UserEndpoint.routes()


class ExpenseEndpoint(BaseEndpoint):
	MODEL = models.Expense
	INITIAL_ROUTES = UserProfileRelationEndpoint.routes()

	@classmethod
	async def expense_per_month(cls, request: Request):

		expenses = await models.Expense.items()
		months = map(lambda x: (x.payment_date.year, x.payment_date.month), expenses)

		result = dict()
		for item in months:
			result[item] = list(filter(lambda x: (x.payment_date.year, x.payment_date.month) == item, expenses))

		text = Title('Valor Total de Despesas').__str__()

		for key, value in result.items():
			text += Title(f'{key[0]}/{key[1]}: {reduce(lambda x, y: x + y, [item.payment_value for item in value]).__round__(2)}', 3, bootstrap='text-dark bg-white').__str__()
		text += '<hr>'
		temp = templates.get_template('model/list.jj').render(**cls.model().template_data(request), sum=Markup(text))
		return HTMLResponse(Markup(temp))

	@classmethod
	async def expense_per_cost_type(cls, request: Request):
		expenses = await models.Expense.items()

		title = Title('Valor Total de Despesas por Tipo de Custo', 1, bootstrap='text-white').__str__()
		years = {item.payment_date.year for item in expenses}
		years_list = list()
		for year in years:
			total = Money(reduce(lambda x, y: x + y, [item.payment_value for item in expenses if
			                                          item.payment_date.year == year], 0).__round__(2))

			year_title = Title(f'Ano {year} (total {total})', 3, bootstrap='text-white').__str__()
			months_list = list()
			months = {item.payment_date.month for item in expenses}
			for month in months:
				total = Money(
					reduce(lambda x, y: x + y,
					       [item.payment_value
					        for item in expenses
					        if item.payment_date.year == year and item.payment_date.month == month], 0).__round__(2)
				)
				month_title = Title(f'Mês {Month(month)} (total {total})', 5, bootstrap='bg-dark text-white').__str__()
				costs = {item.cost_type for item in expenses}
				costs_list = list()
				for key in costs:
					costs_list.append(
						ListGroupItem(
							key.value + ': ' + Money(reduce(lambda x, y: x + y, [item.payment_value for item in expenses if item.cost_type == key and item.payment_date.month == month and item.payment_date.year == year], 0).__round__(2)).__str__()))
				months_list.append(
					ListGroup(month_title, items=costs_list)
				)
			years_list.append(
				ListGroup(year_title, items=months_list)
			)
		text = ListGroup(title=title, items=years_list).__str__()
		temp = templates.get_template('model/list.jj').render(**cls.model().template_data(request), sum=Markup(text))
		return HTMLResponse(Markup(temp))

	@classmethod
	async def expense_per_employee(cls, request: Request):

		expenses = await models.Expense.items()
		employees_expenses = [item for item in list(filter(lambda x: x.employee_key not in [None, ''], expenses)) if item.employee.full_name != 'Daniel Victor Arantes']

		class EmployeeExpense(NamedTuple):
			year: int
			month: int
			employee: MODEL_MAP['Employee']
			expense: MODEL_MAP['Expense']

		items = [EmployeeExpense(x.payment_date.year, x.payment_date.month, x.employee, x) for x in employees_expenses]
		title = Title('Valor Total de Despesas por Funcionário ou Contratado', 1, bootstrap='text-white').__str__()
		years = {item.year for item in items}
		years_list = list()
		for year in years:
			total = Money(reduce(lambda x, y: x + y, [item.payment_value for item in employees_expenses if
			                                          item.payment_date.year == year], 0).__round__(2))

			year_title = Title(f'Ano {year} (total {total})', 3, bootstrap='text-white').__str__()
			months_list = list()
			months = {item.month for item in items}
			for month in months:
				total = Money(
					reduce(lambda x, y: x + y,
					       [item.payment_value
					        for item in employees_expenses
					        if item.payment_date.year == year and item.payment_date.month == month], 0).__round__(2)
				)
				month_title = Title(f'Mês {Month(month)} (total {total})', 5, bootstrap='bg-dark text-white').__str__()
				employees = {item.employee.key for item in items}
				employees_list = list()
				for key in employees:
					employees_list.append(
						ListGroupItem(
							str(MODEL_MAP['Employee'](**templates.env.globals['Employee'][key]).full_name) + ': ' + Money(reduce(lambda x, y: x + y, [item.payment_value for item in employees_expenses if item.employee_key == key and item.payment_date.month == month and item.payment_date.year == year], 0).__round__(2)).__str__()))
				months_list.append(
					ListGroup(month_title, items=employees_list)
				)
			years_list.append(
				ListGroup(year_title, items=months_list)
			)
		text = ListGroup(title=title, items=years_list).__str__()
		temp = templates.get_template('model/list.jj').render(**cls.model().template_data(request), sum=Markup(text))
		return HTMLResponse(Markup(temp))



	@classmethod
	def additional_routes(cls) -> list[Union[Mount, Route]]:
		return [
			Route('/list/sum', cls.expense_per_month),
			Route('/list/employee', cls.expense_per_employee),
			Route('/list/cost', cls.expense_per_cost_type)

		]


class InvoiceEndpoint(BaseEndpoint):
	MODEL = models.Invoice
	INITIAL_ROUTES = ExpenseEndpoint.routes()


class ConciergeEndpoint(BaseEndpoint):
	MODEL = models.Concierge
	INITIAL_ROUTES = InvoiceEndpoint.routes()


class ServiceEndpoint(BaseEndpoint):
	MODEL = models.Service
	INITIAL_ROUTES = ConciergeEndpoint.routes()


class FacilityEndpoint(BaseEndpoint):
	MODEL = models.Facility
	INITIAL_ROUTES = ServiceEndpoint.routes()


class DepositEndpoint(BaseEndpoint):
	MODEL = models.Deposit
	INITIAL_ROUTES = FacilityEndpoint.routes()


class MedicalVisitEndpoint(BaseEndpoint):
	MODEL = models.MedicalVisit
	INITIAL_ROUTES = DepositEndpoint.routes()


class Home(HTTPEndpoint):
	FINAL_ROUTES = MedicalVisitEndpoint.routes()


	@classmethod
	def additional_routes(cls) -> list[Union[Mount, Route]]:
		return list()


	@staticmethod
	async def logged(request: Request):
		await ctx_update()
		return templates.TemplateResponse('logged.jj', {'request': request, 'models': MODEL_MAP})
	@staticmethod
	async def login(request: Request):
		if request.method == 'GET':
			return templates.TemplateResponse('login.jj', {'request': request, 'models': MODEL_MAP})
		elif request.method == 'POST':
			data = await form_data(request)
			return await login_user(request, data['username'], data['password'])
	@staticmethod
	async def logout(request: Request):
		request.session.clear()
		return RedirectResponse('/')

	@staticmethod
	async def context(request: Request):
		await ModelContext.update_all()
		return templates.TemplateResponse('index.jj', {
			'request': request,
			'models': MODEL_MAP
		})

	@staticmethod
	async def start(request: Request):
		return templates.TemplateResponse('index.jj', {
			'request': request,
			'models': MODEL_MAP
		})

	@classmethod
	def final_routes(cls):
		return cls.FINAL_ROUTES or list()

	@classmethod
	def routes(cls):
		return [
			Route('/', cls.start, name='home'),
			Route('/login', cls.login, name='login', methods=['GET', 'POST']),
			Route('/logout', cls.logout, name='logout', methods=['GET']),
			Route('/logged', cls.logged, name='logged', methods=['GET']),
			Route('/context', cls.context, name='context', methods=['GET']),
			Mount('/static', app=static, name='static'),
			*cls.additional_routes(),
			*cls.final_routes()
		]
