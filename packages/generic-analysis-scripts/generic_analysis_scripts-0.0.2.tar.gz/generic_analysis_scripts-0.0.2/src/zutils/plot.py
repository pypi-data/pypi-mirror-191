import zfit
import mplhep
import hist
import numpy             as np
import matplotlib.pyplot as plt
import tensorflow        as tf
import utils_noroot      as utnr
import warnings

#----------------------------------------
class plot:
    log = utnr.getLogger(__name__)
    #----------------------------------------
    def __init__(self, data=None, model=None, result=None, suffix=''):
        """
        obs: zfit space you are using to define the data and model
        data: the data you are fit on
        total_model: the final total fit model
        """

        if isinstance(data, np.ndarray):
            data = zfit.Data.from_numpy(obs=model.space, array=data)

        self.obs               = model.space 
        self.data              = data
        self.total_model       = model
        self.lower, self.upper = self.data.data_range.limit1d
        self.x                 = np.linspace(self.lower, self.upper, 2000)
        self.data_np           = zfit.run(zfit.z.unstack_x(self.data))
        self.binned_data       = None
        self.errors            = []
        self._result           = result
        self._suffix           = suffix
        self._leg              = {}
        self.axs               = None

        # zfit.settings.advanced_warnings['extend_wrapped_extended'] = False
        warnings.filterwarnings("ignore")
    #----------------------------------------
    def _plot_model(self, ax, model, yields, nbins=100, linestyle="-"):
        y = model.pdf(self.x) * yields / nbins * (self.upper - self.lower)
        ax.plot(self.x, y, linestyle, label=self._leg.get(model.name, model.name))
    #----------------------------------------
    def _get_errors(self, data_hist, errorbars, nbins):
        lines = errorbars[0].errorbar[2]
        segs = lines[0].get_segments()
        values = data_hist.values()
        for i in range(nbins):
            low = values[i] - segs[i][0][1]
            up = segs[i][1][1] - values[i]
            self.errors.append((low, up))
    #----------------------------------------
    def _plot_data(self, ax, nbins=100):
        data_hist = hist.Hist(
            hist.axis.Regular(nbins, self.lower, self.upper, name=self.obs.obs[0], underflow=False, overflow=False)
        )
        data_hist.fill(self.data_np)
        self.binned_data = data_hist
        errorbars = mplhep.histplot(
            data_hist,
            yerr=True,
            color="black",
            histtype="errorbar",
            label=self._leg.get("Data", "Data"),
            ax=ax,
        )
        self._get_errors(data_hist, errorbars, nbins)
    #----------------------------------------
    def _pull_hist(self, pdf_hist, nbins):
        old_yield = pdf_hist.sum().value
        new_yield = self.binned_data.sum()
        pdf_values = pdf_hist.values()
        data_values = self.binned_data.values()
        pull_errors = [[], []]
        pulls = []
        for i in range(nbins):
            p = data_values[i] - pdf_values[i]*new_yield/old_yield
            low = self.errors[i][0]
            up = self.errors[i][1]
            if p > 0:
                e = low
            else:
                e = up
            pulls.append(p / e)
            pull_errors[0].append(low / e)
            pull_errors[1].append(up / e)
        pull_hist = hist.Hist(
            hist.axis.Regular(nbins, self.lower, self.upper, name="pulls")
        )
        pull_hist[0:nbins] = pulls
        return pull_hist, pull_errors
    #----------------------------------------
    def _plot_pulls(self, ax, nbins=100):
        obs_name = self.obs.obs[0]
        binning = zfit.binned.RegularBinning(
            bins=nbins, start=self.lower, stop=self.upper, name=obs_name
        )
        binned_obs  = zfit.Space(obs_name, binning=binning)
        binned_pdf  = zfit.pdf.BinnedFromUnbinnedPDF(
            self.total_model, binned_obs
        )

        pdf_hist = binned_pdf.to_hist()
        pull_hist, pull_errors = self._pull_hist(pdf_hist, nbins)
        mplhep.histplot(
            pull_hist,
            color="black",
            histtype="errorbar",
            yerr=np.array(pull_errors),
            ax=ax,
        )
    #----------------------------------------
    def _get_zfit_gof(self):
        if not hasattr(self._result, 'gof'):
            return
    
        chi2, ndof, pval = self._result.gof
    
        rchi2 = chi2/ndof
    
        return f'$\chi^2$/NdoF={chi2:.2f}/{ndof}={rchi2:.2f}\np={pval:.3f}'
    #----------------------------------------
    def _get_text(self, ext_text):
        gof_text = self._get_zfit_gof()

        if   ext_text is     None and gof_text is     None:
            return
        elif ext_text is not None and gof_text is     None:
            return ext_text
        elif ext_text is     None and gof_text is not None:
            return gof_text
        else:
            return f'{ext_text}\n{gof_text}'
    #----------------------------------------
    def plot(self, nbins: int=100, unit: str="$\\rm{MeV}/\\it{c}^{2}$", xlabel: str="", ylabel: str="", d_leg: dict={}, plot_range: tuple = None, ext_text : str = None):
        """
        nbins: bin numbers
        unit: Unit for x axis, default is MeV/c^2
        xlabel: xlabel
        ylabel: ylabel
        d_leg: customize legend
        plot_range: set plot_range
        ext_text: text that can be added to plot
        """
        if plot_range is not None:
            try:
                self.lower, self.upper = plot_range
            except TypeError:
                self.log.error(f'plot_range argument is expected to be a tuple with two numeric values')
                raise TypeError

            self.x = np.linspace(self.lower, self.upper, 2000)

        plt.style.use(mplhep.style.LHCb2)
        fig       = plt.figure()
        gs        = fig.add_gridspec(nrows=2, ncols=1, hspace=0.1, height_ratios=[4, 1])
        axs       = gs.subplots(sharex=True)
        self._leg = d_leg
        self.axs  = axs
        self._plot_model(axs[0], self.total_model, tf.cast(self.data.nevents, dtype=tf.float64), nbins,)

        l_model = self.total_model.pdfs if hasattr(self.total_model, 'pdfs') else []

        for model in l_model: 
            yld_par = None if not model.is_extended else model.get_yield()
            if yld_par is None:
                continue

            nevs = yld_par.value()

            self._plot_model(axs[0], model, tf.cast(nevs, dtype=tf.float64), nbins, "--",)

        self._plot_data(axs[0], nbins)
        self._plot_pulls(axs[1], nbins)

        if xlabel == "":
            xlabel = f"{self.obs.obs[0]} [{unit}]"

        if ylabel == "":
            ylabel = f"Candidates / ({(self.upper-self.lower)/nbins} {unit})"

        text=self._get_text(ext_text)

        axs[0].legend(title=text, fontsize=20, title_fontsize=20)
        axs[0].set(xlabel=xlabel, ylabel=ylabel)
        axs[0].set_xlim([self.lower, self.upper])

        axs[1].set(xlabel=xlabel, ylabel="pulls")
        axs[1].set_xlim([self.lower, self.upper])

        for ax in axs.flat:
            ax.label_outer()
#----------------------------------------

