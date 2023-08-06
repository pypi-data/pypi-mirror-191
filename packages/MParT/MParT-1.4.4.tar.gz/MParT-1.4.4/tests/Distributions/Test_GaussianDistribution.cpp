#include <algorithm>
#include <catch2/catch_all.hpp>
#include "MParT/Utilities/ArrayConversions.h"
#include "MParT/Distributions/GaussianSamplerDensity.h"

using namespace mpart;
using namespace Catch;

// Tests samples that should be transformed to a standard normal distribution
void TestStandardNormalSamples(StridedMatrix<double, Kokkos::HostSpace> samples) {
    unsigned int dim = samples.extent(0);
    unsigned int N_samp = samples.extent(1);
    double mc_margin = (1/std::sqrt(N_samp))*10.0;

    Distribution<Kokkos::HostSpace> dist = CreateGaussianDistribution<Kokkos::HostSpace>(dim);
    Kokkos::View<double*, Kokkos::HostSpace> mean("mean", dim);
    Kokkos::View<double**, Kokkos::HostSpace> covar("covar", dim, dim);
    std::fill(mean.data(), mean.data()+dim, 0.0);
    std::fill(covar.data(), covar.data()+dim*dim, 0.0);
    // Calculate sample mean and sample covariance
    for(int i = 0; i < N_samp; i++) {
        for(int j = 0; j < dim; j++) {
            mean(j) += samples(j, i)/N_samp;
            for(int k = 0; k < dim; k++) {
                covar(j, k) += samples(j, i) * samples(k, i)/(N_samp-1);
            }
        }
    }

    // Check that the mean is zero and the covariance is the identity matrix
    for(int i = 0; i < dim; i++) {
        REQUIRE(mean(i) == Approx(0.0).margin(mc_margin));
        for(int j = 0; j < dim; j++) {
            double diag = (double) (i == j);
            REQUIRE(covar(i, j) - mean(i)*mean(j) == Approx(diag).margin(mc_margin));
        }
    }

    std::vector<unsigned int> in_one_std (dim, 0);
    std::vector<unsigned int> in_two_std (dim, 0);
    std::vector<unsigned int> in_three_std (dim, 0);
    for(int i = 0; i < N_samp; i++) {
        for(int j = 0; j < dim; j++) {
            double samp_abs = std::abs(samples(j, i));
            if(samp_abs < 1.0) {
                in_one_std[j]++;
            }
            if(samp_abs < 2.0) {
                in_two_std[j]++;
            }
            if(samp_abs < 3.0) {
                in_three_std[j]++;
            }
        }
    }
    double emp_one_std = 0.682689492137;
    double emp_two_std = 0.954499736104;
    double emp_three_std = 0.997300203937;
    for(int i = 0; i < dim; i++) {
        REQUIRE(in_one_std[i]/(double)N_samp == Approx(emp_one_std).margin(mc_margin));
        REQUIRE(in_two_std[i]/(double)N_samp == Approx(emp_two_std).margin(mc_margin));
        REQUIRE(in_three_std[i]/(double)N_samp == Approx(emp_three_std).margin(mc_margin));
    }
}

// Tests samples that should be transformed to a standard normal distribution and the pdf of the samples prior to transformation
void TestGaussianLogPDF(StridedMatrix<double, Kokkos::HostSpace> samples, StridedVector<double, Kokkos::HostSpace> samples_pdf,
        StridedMatrix<double, Kokkos::HostSpace> samples_gradpdf, double logdet_cov, double sqrt_diag, double abs_margin) {
    unsigned int dim = samples.extent(0);
    unsigned int N_samp = samples.extent(1);

    double offset = -0.9189385332046728*dim; // -log(2*pi)*dim/2
    offset -= 0.5*logdet_cov;
    // Calculate difference of samples_pdf and the true pdf in place
    Kokkos::parallel_for(N_samp, KOKKOS_LAMBDA(const int i) {
        double norm = 0.;
        for(int j = 0; j < dim; j++) {
            norm += samples(j, i)*samples(j, i);
            samples_gradpdf(j,i) += samples(j, i)/sqrt_diag;
            samples_gradpdf(j,i) = std::abs(samples_gradpdf(j,i));
        }
        samples_pdf(i) -= offset - 0.5*norm;
        samples_pdf(i) = std::abs(samples_pdf(i));
    });
    // Find the maximum difference and assert it's within the margin of error
    double max_pdf_err = *std::max_element(samples_pdf.data(), samples_pdf.data()+N_samp);
    double max_gradpdf_err = *std::max_element(samples_gradpdf.data(), samples_gradpdf.data()+N_samp*dim);
    REQUIRE(max_pdf_err < abs_margin);
    REQUIRE(max_gradpdf_err < abs_margin);
}

TEST_CASE( "Testing Gaussian Distribution", "[GaussianDist]") {
    unsigned int dim = 3;
    unsigned int N_samp = 5000;
    double covar_diag_val = 4.0;
    double abs_margin = 1e-6;

    SECTION( "Default Covariance, Default mean" ) {
        Distribution<Kokkos::HostSpace> dist = CreateGaussianDistribution<Kokkos::HostSpace>(dim);
        Kokkos::View<double**, Kokkos::LayoutLeft, Kokkos::HostSpace> samples ("sample matrix", dim, N_samp);
        Kokkos::View<double*, Kokkos::LayoutLeft, Kokkos::HostSpace> samples_pdf ("sample pdf", N_samp);
        Kokkos::View<double**, Kokkos::LayoutLeft, Kokkos::HostSpace> samples_gradpdf ("sample grad pdf", dim, N_samp);
        dist.SampleImpl(samples);
        dist.LogDensityImpl(samples, samples_pdf);
        dist.LogDensityInputGradImpl(samples, samples_gradpdf);
        TestStandardNormalSamples(samples);
        TestGaussianLogPDF(samples, samples_pdf, samples_gradpdf, 0., 1., abs_margin);
    }


    Kokkos::View<double*, Kokkos::HostSpace> mean("mean", dim);
    std::fill(mean.data(), mean.data()+dim, 1.0);

    SECTION( "Default Covariance, unit mean in all dimensions" ) {
        Distribution<Kokkos::HostSpace> dist = CreateGaussianDistribution<Kokkos::HostSpace>(mean);
        Kokkos::View<double**, Kokkos::LayoutLeft, Kokkos::HostSpace> samples ("sample matrix", dim, N_samp);
        Kokkos::View<double*, Kokkos::LayoutLeft, Kokkos::HostSpace> samples_pdf ("sample pdf", N_samp);
        Kokkos::View<double**, Kokkos::LayoutLeft, Kokkos::HostSpace> samples_gradpdf ("sample grad pdf", dim, N_samp);
        dist.SampleImpl(samples);
        dist.LogDensityImpl(samples, samples_pdf);
        dist.LogDensityInputGradImpl(samples, samples_gradpdf);
        Kokkos::parallel_for(dim, KOKKOS_LAMBDA(const int i) {
            for(int j = 0; j < N_samp; j++) {
                samples(i, j) -= 1.0;
            }
        });
        TestStandardNormalSamples(samples);
        TestGaussianLogPDF(samples, samples_pdf, samples_gradpdf, 0., 1., abs_margin);
    }

    Kokkos::View<double**, Kokkos::LayoutLeft, Kokkos::HostSpace> covar("covar", dim, dim);
    auto policy = Kokkos::MDRangePolicy<Kokkos::Rank<2>>({0, 0}, {dim, dim});
    Kokkos::parallel_for(policy, KOKKOS_LAMBDA(const int i, const int j) {
        covar(i, j) = ((double) (i == j))*covar_diag_val;
    });

    SECTION( "Diagonal Covariance, Default mean" ) {
        Distribution<Kokkos::HostSpace> dist = CreateGaussianDistribution<Kokkos::HostSpace>(covar);
        Kokkos::View<double**, Kokkos::LayoutLeft, Kokkos::HostSpace> samples ("sample matrix", dim, N_samp);
        Kokkos::View<double*, Kokkos::LayoutLeft, Kokkos::HostSpace> samples_pdf ("sample pdf", N_samp);
        Kokkos::View<double**, Kokkos::LayoutLeft, Kokkos::HostSpace> samples_gradpdf ("sample grad pdf", dim, N_samp);
        dist.SampleImpl(samples);
        dist.LogDensityImpl(samples, samples_pdf);
        dist.LogDensityInputGradImpl(samples, samples_gradpdf);
        policy = Kokkos::MDRangePolicy<Kokkos::Rank<2>>({0, 0}, {dim, N_samp});
        Kokkos::parallel_for(policy, KOKKOS_LAMBDA(const int i, const int j) {
            samples(i, j) /= std::sqrt(covar_diag_val);
        });
        TestStandardNormalSamples(samples);
        TestGaussianLogPDF(samples, samples_pdf, samples_gradpdf, dim*std::log(covar_diag_val), std::sqrt(covar_diag_val), abs_margin);
    }

    SECTION( "Diagonal Covariance, unit mean in all dimensions" ) {
        Distribution<Kokkos::HostSpace> dist = CreateGaussianDistribution<Kokkos::HostSpace>(mean, covar);
        Kokkos::View<double**, Kokkos::LayoutLeft, Kokkos::HostSpace> samples ("sample matrix", dim, N_samp);
        Kokkos::View<double*, Kokkos::LayoutLeft, Kokkos::HostSpace> samples_pdf ("sample pdf", N_samp);
        Kokkos::View<double**, Kokkos::LayoutLeft, Kokkos::HostSpace> samples_gradpdf ("sample grad pdf", dim, N_samp);
        dist.SampleImpl(samples);
        dist.LogDensityImpl(samples, samples_pdf);
        dist.LogDensityInputGradImpl(samples, samples_gradpdf);
        policy = Kokkos::MDRangePolicy<Kokkos::Rank<2>>({0, 0}, {dim, N_samp});
        Kokkos::parallel_for(policy, KOKKOS_LAMBDA(const int i, const int j) {
            samples(i, j) -= 1.0;
            samples(i, j) /= std::sqrt(covar_diag_val);
        });
        TestStandardNormalSamples(samples);
        TestGaussianLogPDF(samples, samples_pdf, samples_gradpdf, dim*std::log(covar_diag_val), std::sqrt(covar_diag_val), abs_margin);
    }
}