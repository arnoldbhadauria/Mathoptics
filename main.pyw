import flet as ft
import sympy as sp
# from matplotlib.container import Container
from sympy import log, exp, simplify, sin, cos, tan, sec, cot, sinc, asin, acos, atan, acsc, asec, acot, Eq, solve, \
    symbols, content
import matplotlib.pyplot as plt
import numpy as np
import re
import io
import base64

blank_base64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8"
    "/5+hHgAHggJ/PqV6KQAAAABJRU5ErkJggg=="
)

def main(page: ft.Page):
    page.title = "Math Master App"
    # page.theme_mode = 'dark-theme'
    page.window.maximized = True
    page.window_width = 400
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT

    app_font = 'Inter'
    equation_font = 'Consolas'

    white_color = ft.colors.WHITE
    black_color = ft.colors.BLACK

    equations = []
    x, y, z = symbols('x y z')

    def go_home(_=None):
        page.views.clear()
        page.views.append(home_view())
        page.update()

    def home_view():
        calculus_btn = ft.ElevatedButton(
            content=ft.Row(
                [ft.Text("Calculus", color=white_color, font_family=app_font, size=14)],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            bgcolor=black_color,
            on_click=lambda _: page.go("/calculus"),
            width=250,
            height=50,
        )
        equation_btn = ft.ElevatedButton(
            content=ft.Row(
                [ft.Text("Equation Solver", color=white_color, font_family=app_font, size=14)],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,

            ),
            bgcolor=black_color,
            on_click=lambda _: page.go("/linear"),
            width=250,
            height=50,
        )
        quadratic_btn = ft.ElevatedButton(
            content=ft.Row(
                [ft.Text("Quadratic", color=white_color, font_family=app_font, size=14)],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            bgcolor=black_color,
            on_click=lambda _: page.go("/quadratic"),
            width=250,
            height=50,
        )
        graph_btn = ft.ElevatedButton(
            content=ft.Row(
                [ft.Text("Graph", color=white_color, font_family=app_font, size=14)],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            bgcolor=black_color,
            on_click=lambda _: page.go("/graph"),
            width=250,
            height=50,
        )

        main_container = ft.Container(
            ft.Column(
                [calculus_btn, equation_btn, quadratic_btn, graph_btn]
            ),
            padding=20,
            # border=ft.border.all(1, black_color),
            alignment=ft.alignment.center
        )

        head = ft.Container(
            content=ft.Text("Functions", size=20, font_family=app_font),
            padding=20,
            alignment=ft.alignment.center
        )
        divider = ft.Divider()
        return ft.View(
            "/",
            controls=[
                ft.AppBar(title=ft.Text("Mathoptics", font_family=app_font, color=white_color), bgcolor=black_color),
                ft.Container(
                    ft.Column(
                        [
                            head, divider, main_container
                        ]
                    ),
                    padding=20,
                    border=ft.border.all(1, black_color),
                    width=450,
                    border_radius=20
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def calculus_view():

        def error_message(message):
            snackbar = ft.SnackBar(
                content=ft.Text(f"{message}", size=16, font_family=app_font, color=white_color),
                bgcolor=ft.colors.RED
            )
            page.open(snackbar)
            page.update()

        def parse_expression(expression):
            expression = expression.replace("e", "exp")
            expression = re.sub(r'(\d)([a-zA-Z])', r'\1 * \2', expression)
            expression = expression.replace("^", "**")
            return expression

        def deparse_expression(expression):
            expression = expression.replace("**", "^").replace("*", "")
            expression = expression.replace("exp", "e")
            return expression

        def clear_differentiation(e):
            diff_textbox.value = ""
            diff_solution.value = ""
            page.update()

        def clear_integration(e):
            int_textbox.value = ""
            int_solution.value = ""
            page.update()

        def calculate_differentiation(e):
            if diff_textbox.value.strip() == "":
                error_message("Invalid Input.")
            else:
                try:
                    user_exp = diff_textbox.value
                    user_exp = parse_expression(user_exp)
                    #
                    user_exp = simplify(user_exp)

                    answer = sp.diff(eval(str(user_exp)), x)

                    answer = str(answer)
                    answer = deparse_expression(answer)
                    diff_solution.value = f"{answer}"
                    page.update()
                except:
                    error_message("This calculation is outside the recommended complexity range.")

        def calculate_integration(e):
            if int_textbox.value.strip() == "":
                error_message("Invalid Input")
            else:
                try:
                    user_exp = int_textbox.value
                    user_exp = parse_expression(user_exp)
                    #
                    user_exp = simplify(user_exp)

                    answer = sp.integrate(eval(str(user_exp)), x)

                    answer = str(answer)
                    answer = deparse_expression(answer)
                    int_solution.value = f"{answer}"
                    page.update()
                except:
                    error_message("This calculation is outside the recommended complexity range.")

        diff_head = ft.Container(
            content=ft.Text("Differentiation", size=30, font_family=app_font),
            height=50
        )

        divider = ft.Divider()

        diff_textbox = ft.TextField(
            hint_text="Type your expression here...",
            text_size=16,
            text_style=ft.TextStyle(
                font_family=equation_font
            ),
            border_radius=15,
            border_color=black_color,
            expand=True
        )
        diff_solution = ft.Text("", size=16, font_family=equation_font)

        diff_expression = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("f(x) : ", size=20, font_family=app_font),
                    diff_textbox
                ]
            ),
            height=100
        )
        diff_solution_head = ft.Text("Differentiated Expression :", size=18, font_family=app_font)
        diff_solution_container = ft.Container(
            content=ft.Column(
                controls=[
                    diff_solution_head,
                    ft.Row(
                        controls=[
                            ft.Text("f'(x) :: ", size=20, font_family=app_font),
                            diff_solution
                        ]
                    )
                ]
            )
        )
        diff_solve_btn = ft.ElevatedButton(
            content=ft.Text("Solve", size=14, font_family=app_font, color=white_color),
            style=ft.ButtonStyle(
                bgcolor=black_color
            ),
            on_click=calculate_differentiation,
            expand=True
        )
        diff_clear_btn = ft.ElevatedButton(
            content=ft.Text("Clear", size=14, font_family=app_font, color=black_color),
            style=ft.ButtonStyle(
                bgcolor=white_color
            ),
            on_click=clear_differentiation
        )
        diff_btn_container = ft.Container(
            content=ft.Row(
                controls=[diff_solve_btn, diff_clear_btn]
            ),
            height=60
        )

        differentiation_container = ft.Container(
            content=ft.Column(
                controls=[diff_head, divider, diff_expression, diff_solution_container, diff_btn_container]
            ),
            width=500,
            border=ft.border.all(1, black_color),
            padding=25,
            border_radius=15
        )
        int_head = ft.Container(
            content=ft.Text("Integration", size=30, font_family=app_font),
            height=50
        )
        int_textbox = ft.TextField(
            hint_text="Type your expression here...",
            text_size=16,
            text_style=ft.TextStyle(
                font_family=equation_font
            ),
            border_radius=15,
            border_color=black_color,
            expand=True
        )
        int_solution = ft.Text("", size=16, font_family=equation_font)

        int_expression = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("f(x) : ", size=20, font_family=app_font),
                    int_textbox
                ]
            ),
            height=100
        )
        int_solution_head = ft.Text("Integrated Expression :", size=18, font_family=app_font)
        int_solution_container = ft.Container(
            content=ft.Column(
                controls=[
                    int_solution_head,
                    ft.Row(
                        controls=[
                            ft.Text("∫ f(x).dx :: ", size=20, font_family=app_font),
                            int_solution
                        ]
                    )
                ]
            )
        )
        int_solve_btn = ft.ElevatedButton(
            content=ft.Text("Solve", size=14, font_family=app_font, color=white_color),
            style=ft.ButtonStyle(
                bgcolor=black_color
            ),
            on_click=calculate_integration,
            expand=True
        )
        int_clear_btn = ft.ElevatedButton(
            content=ft.Text("Clear", size=14, font_family=app_font, color=black_color),
            style=ft.ButtonStyle(
                bgcolor=white_color
            ),
            on_click=clear_integration
        )
        int_btn_container = ft.Container(
            content=ft.Row(
                controls=[int_solve_btn, int_clear_btn]
            ),
            height=60
        )

        integration_container = ft.Container(
            content=ft.Column(
                controls=[int_head, divider, int_expression, int_solution_container, int_btn_container]
            ),
            width=500,
            border=ft.border.all(1, black_color),
            padding=25,
            border_radius=15
        )
        main_container = ft.Container(
            content=ft.Row(
                controls=[differentiation_container, integration_container]
            ),
            alignment=ft.alignment.center,
            width=1060,
            # border=ft.border.all(1, white_color),
            padding=25,
            border_radius=25
        )
        page.update()

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Calculus", size=14, font_family=app_font, color=white_color),
                          bgcolor=black_color,
                          leading=ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=white_color, on_click=go_home)),
                main_container],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    # LINEAR EQUATIONS -------------------------------------------------------------------------------

    def linear_view():
        def error_message(message):
            snackbar = ft.SnackBar(
                content=ft.Text(f"{message}", size=14, color=ft.colors.WHITE, font_family=app_font),
                bgcolor=ft.colors.RED
            )
            page.open(snackbar)

        coeff_x = ft.TextField(label="a", text_size=20, width=100, border_color=black_color, border_radius=50,
                               text_align=ft.alignment.center, text_style=ft.TextStyle(font_family=app_font))
        coeff_y = ft.TextField(label='b', text_size=20, width=100, border_color=black_color, border_radius=50,
                               text_align=ft.alignment.center, text_style=ft.TextStyle(font_family=app_font))
        coeff_z = ft.TextField(label='c', text_size=20, width=100, border_color=black_color, border_radius=50,
                               text_align=ft.alignment.center, text_style=ft.TextStyle(font_family=app_font))
        constant = ft.TextField(label='d', text_size=20, width=100, border_color=black_color, border_radius=50,
                                text_align=ft.alignment.center, text_style=ft.TextStyle(font_family=app_font))

        def solve_equation(e):
            if len(equations) == 3:
                if len(solutions_container.content.controls) == 0:
                    solutions = solve(equations, (x, y, z))
                    x_value = solutions[x]
                    y_value = solutions[y]
                    z_value = solutions[z]
                    solution_container = ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(f">   x = {x_value}", size=18, font_family=app_font),
                                ft.Text(f">   y = {y_value}", size=18, font_family=app_font),
                                ft.Text(f">   z = {z_value}", size=18, font_family=app_font)
                            ]
                        )
                    )
                    solutions_container.content.controls.append(solution_container)
                    page.update()
                else:
                    pass
            else:
                error_message("3 equations required.")

        def clear_container(e):
            equations_container.content.controls.clear()
            solutions_container.content.controls.clear()
            equations.clear()
            page.update()

        def add_equation(e):
            if coeff_x.value.isdigit() and coeff_y.value.isdigit() and coeff_z.value.isdigit() and constant.value.isdigit():
                if int(coeff_x.value) == 0 and int(coeff_y.value) == 0 and int(coeff_z.value) == 0 and int(
                        constant.value) == 0:
                    error_message("All coefficients cannot be zero.")
                else:
                    new_equation_container = ft.Container(
                        content=ft.Text(
                            f" >   ({coeff_x.value})x + ({coeff_y.value})y + ({coeff_z.value})z = ({constant.value})",
                            size=18, font_family=app_font)
                    )
                    equations.append(
                        Eq(int(coeff_x.value) * x + int(coeff_y.value) * y + int(coeff_z.value) * z,
                           int(constant.value)))
                    equations_container.content.controls.append(new_equation_container)
                    coeff_x.value = ""
                    coeff_y.value = ""
                    coeff_z.value = ""
                    constant.value = ""
                    page.update()
            else:
                error_message("Invalid Input")

        add_btn = ft.ElevatedButton(
            content=ft.Row(
                [ft.Text("Add", color=white_color, size=18, font_family=app_font)],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            bgcolor=black_color,
            width=200,
            height=50,
            # content=ft.Text("Add", size=20, width=100, text_align=ft., color=ft.colors.BLACK),
            # bgcolor=ft.colors.WHITE,
            on_click=add_equation,
            # height=50
        )

        solve_btn = ft.ElevatedButton(
            content=ft.Text("Solve", size=14, font_family=app_font, color=white_color),
            bgcolor=black_color,
            height=50,
            expand=True,
            on_click=solve_equation
        )
        clear_btn = ft.ElevatedButton(
            content=ft.Text("Clear", size=14, font_family=app_font, color=black_color),
            bgcolor=white_color,
            height=50,
            on_click=clear_container
            # expand=True
        )
        buttons_container = ft.Container(
            content=ft.Row(
                controls=[solve_btn, clear_btn]
            ),
            padding=15
        )

        equations_head = ft.Container(
            content=ft.Text("Equations :", size=16, font_family=app_font),
            padding=15
        )
        solutions_head = ft.Container(
            content=ft.Text("Solutions :", size=16, font_family=app_font),
            padding=15
        )

        heading = ft.Container(
            content=ft.Text("Three-Variables Equation Solver", size=25, font_family=app_font),
            padding=15
        )

        equation = ft.Container(
            content=ft.Row(
                controls=[
                    coeff_x,
                    ft.Text("X  +  ", font_family=app_font, size=23),
                    coeff_y,
                    ft.Text("Y  +  ", font_family=app_font, size=23),
                    coeff_z,
                    ft.Text("Z  =  ", font_family=app_font, size=23),
                    constant
                ]
            ),
            padding=15,
            border_radius=50,
            border=ft.border.all(1, ft.colors.WHITE),
            expand=True
        )

        eq_creator_container = ft.Container(
            content=ft.Row(
                controls=[equation, add_btn]
            ),
            padding=15
        )
        equations_container = ft.Container(
            content=ft.Column(
                controls=[]
            )
        )
        solutions_container = ft.Container(
            content=ft.Column(
                controls=[]
            )
        )
        divider = ft.Divider()

        main_container = ft.Container(
            content=ft.Column(
                controls=[heading, divider, eq_creator_container, equations_head, equations_container, solutions_head,
                          solutions_container,
                          buttons_container]
            ),
            width=1000,
            padding=15,
            alignment=ft.alignment.center,
            border=ft.border.all(1, black_color),
            border_radius=20
        )
        page_container = ft.Container(
            content=main_container,
            alignment=ft.alignment.center
        )

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Equation Solver", size=14, font_family=app_font, color=white_color),
                          bgcolor=black_color,
                          leading=ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=white_color, on_click=go_home)),
                page_container
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            auto_scroll=True
        )

    def quadratic_view():
        a = ft.TextField(label="a", width=100, border_radius=20)
        b = ft.TextField(label="b", width=100, border_radius=20)
        c = ft.TextField(label="c", width=100, border_radius=20)
        result = ft.Text(size=18)
        head = ft.Container(
            content=ft.Text("Quadratic Equation", size=24, font_family=app_font),
            padding=20
        )
        divider = ft.Divider()
        equation_box = ft.Container(
            content=ft.Row(
                controls=[
                    a,
                    ft.Text(f"x^2  +  ", size=16, font_family=app_font),
                    b,
                    ft.Text(f"x  +  ", size=16, font_family=app_font),
                    c,
                    ft.Text(f"  =  ", size=16, font_family=app_font),
                    ft.Text("0", size=16, font_family=app_font),
                ]
            )
        )
        solution_head = ft.Text("Solution:", size=17, font_family=app_font)
        result_box = ft.Container(
            content=result,
            padding=20
        )
        action_box = ft.Container(
            content=ft.Row(
                controls=[
                    ft.ElevatedButton(content=ft.Text("Solve", font_family=app_font, color=white_color), bgcolor=black_color, expand=True, height=50, on_click=lambda e: solve_quadratic(e)),
                    ft.ElevatedButton(content=ft.Text("Clear", font_family=app_font, color=black_color), bgcolor=white_color, width=100, height=50, on_click=lambda e: clear_(e)),
                ]
            )
        )

        def clear_(e):
            result.value = ""
            a.value = ""
            b.value = ""
            c.value = ""
            print("All clear.")
            page.update()

        def solve_quadratic(e):
            try:
                a_val = float(a.value)
                b_val = float(b.value)
                c_val = float(c.value)
                disc = b_val ** 2 - 4 * a_val * c_val
                if disc < 0:
                    result.value = "No real roots"
                else:
                    x1 = (-b_val + disc ** 0.5) / (2 * a_val)
                    x2 = (-b_val - disc ** 0.5) / (2 * a_val)
                    result.value = f"x1 = {x1}, x2 = {x2}"
            except:
                result.value = "Invalid input"
            page.update()

        return ft.View(
            "/quadratic",
            controls=[
                ft.AppBar(title=ft.Text("Quadratic Equation", size=14, color=white_color, font_family=app_font),
                          bgcolor=black_color,
                          leading=ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=white_color, on_click=go_home)),
                ft.Container(
                    content=ft.Column(
                        controls=[head, divider, equation_box, solution_head, result_box, divider, action_box]
                    ),
                    padding=20,
                    width=700,
                    border_radius=20,
                    border=ft.border.all(1, black_color)
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def graph_view():
        input_expr = ft.TextField(label="Enter Equation", autofocus=True, expand=True, border_radius=20, border_color=black_color)
        # result = ft.Image(src="", width=300, height=300)
        graph = ft.Image(src_base64=blank_base64, width=700, height=500, border_radius=20)

        head = ft.Container(
            content=ft.Text("Graph", size=24, font_family=app_font),
            padding=10
        )
        divider = ft.Divider()
        graph_box = ft.Container(
            content=graph,
            alignment=ft.alignment.center
        )
        input_box = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(" f(x) = ", color=black_color, font_family=app_font),
                    input_expr,
                    ft.ElevatedButton(
                        content=ft.Text("Plot", color=white_color, font_family=app_font),
                        on_click=lambda e: plot_equation(e),
                        height=50,
                        width=100,
                        bgcolor=black_color
                    )
                ]
            )
        )
        def plot_equation(e):
            try:
                # Parse the expression from text input
                expr = sp.sympify(input_expr.value)

                # Generate x and y values
                x_vals = np.linspace(-10, 10, 400)
                y_vals = [float(expr.subs(x, val)) for val in x_vals]

                # Plot
                plt.figure()
                plt.plot(x_vals, y_vals, label=f"y = {expr}", color="blue")
                plt.title("Graph of the Equation")
                plt.xlabel("x")
                plt.ylabel("y")
                plt.grid(True)
                plt.legend()

                # Save to buffer
                buf = io.BytesIO()
                plt.savefig(buf, format="png")
                plt.close()
                buf.seek(0)

                # Convert to base64 and display
                img_data = base64.b64encode(buf.read()).decode("utf-8")
                graph.src_base64 = img_data
                page.update()

            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"))
                page.snack_bar.open = True
                page.update()

        return ft.View(
            "/graph",
            controls=[
                ft.AppBar(title=ft.Text("Graph Plotter", size=14, color=white_color, font_family=app_font), bgcolor=black_color,
                          leading=ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=white_color, on_click=go_home)),
                ft.Container(
                    ft.Column(
                        controls=[
                            head, divider, graph_box, divider, input_box
                        ]
                    ),
                    width=800,
                    # height=600,
                    padding=10,
                    border_radius=20,
                    border=ft.border.all(1, black_color)
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    # Route handler
    def route_change(route):
        page.views.clear()
        page.views.append(home_view())
        if page.route == "/calculus":
            page.views.append(calculus_view())
        elif page.route == "/linear":
            page.views.append(linear_view())
        elif page.route == "/quadratic":
            page.views.append(quadratic_view())
        elif page.route == "/graph":
            page.views.append(graph_view())
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


ft.app(target=main)
