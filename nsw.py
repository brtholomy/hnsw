import graphing
import click


@click.command()
@click.option(
    '--nodes', '-n',
    default=20,
    show_default=True,
    help='number of nodes'
)
@click.option(
    '--degree', '-k',
    default=4,
    show_default=True,
    help='degree of nodes'
)
@click.option(
    '--prob', '-p',
    default=0.2,
    show_default=True,
    help='probability of rearranging edges'
)
@click.option(
    '--display', '-d',
    is_flag=True,
    help='whether to display the graphs'
)
@click.option(
    '--save', '-s',
    is_flag=True,
    help='whether to save the graphs as .png files'
)
def Main(nodes, degree, prob, display, save):
    G = graphing.MakeNSW(nodes, degree, prob)

    if display:
        graphing.DrawGraph(G)
        graphing.PlotShow()

    if save:
        graphing.SaveGraph(G, prefix='nsw')


if __name__ == '__main__':
    Main()
