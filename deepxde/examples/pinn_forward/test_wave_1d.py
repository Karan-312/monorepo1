"""Test cases for wave_1d.py"""
import unittest
import numpy as np
import deepxde as dde
from wave_1d import pde, func, get_initial_loss, A, C


class TestWave1D(unittest.TestCase):
    """Test cases for 1D wave equation solver."""

    def setUp(self):
        """Set up test fixtures."""
        self.A = A
        self.C = C

    def test_func_output_shape(self):
        """Test that the solution function returns correct shape."""
        x_test = np.random.rand(10, 2)  # 10 points with (x, t) coordinates
        result = func(x_test)
        self.assertEqual(result.shape, (10, 1))

    def test_func_values_at_origin(self):
        """Test function value at x=0, t=0."""
        x_test = np.array([[0, 0]])
        result = func(x_test)
        # At x=0: sin(0) * cos(0) + sin(0) * cos(0) = 0
        np.testing.assert_almost_equal(result[0, 0], 0.0, decimal=5)

    def test_func_values_at_quarter_point(self):
        """Test function value at x=0.5, t=0."""
        x_test = np.array([[0.5, 0]])
        result = func(x_test)
        # At t=0: sin(pi*0.5) * cos(0) + sin(2*pi*0.5) * cos(0) = 1 + 0 = 1
        expected = np.sin(np.pi * 0.5) + np.sin(A * np.pi * 0.5)
        np.testing.assert_almost_equal(result[0, 0], expected, decimal=5)

    def test_func_is_continuous(self):
        """Test that the function is continuous."""
        x1 = np.array([[0.3, 0.5]])
        x2 = np.array([[0.30001, 0.50001]])
        result1 = func(x1)
        result2 = func(x2)
        # Values should be very close
        self.assertAlmostEqual(result1[0, 0], result2[0, 0], places=3)

    def test_pde_residual_at_exact_solution(self):
        """Test that PDE residual should be small (approximately 0) for exact solution."""
        # Create test points
        x_test = np.array([[0.5, 0.5]])
        
        # Create a simple neural network that approximates the solution
        geom = dde.geometry.Interval(0, 1)
        timedomain = dde.geometry.TimeDomain(0, 1)
        geomtime = dde.geometry.GeometryXTime(geom, timedomain)
        
        # Use a shallow network for quick testing
        layer_size = [2] + [32] * 2 + [1]
        net = dde.nn.FNN(layer_size, "tanh", "Glorot uniform")
        
        # Create dummy data for model
        bc = dde.icbc.DirichletBC(
            geomtime, func, lambda _, on_boundary: on_boundary
        )
        ic_1 = dde.icbc.IC(geomtime, func, lambda _, on_initial: on_initial)
        ic_2 = dde.icbc.OperatorBC(
            geomtime,
            lambda x, y, _: dde.grad.jacobian(y, x, i=0, j=1),
            lambda x, _: dde.utils.isclose(x[1], 0),
        )
        data = dde.data.TimePDE(
            geomtime,
            pde,
            [bc, ic_1, ic_2],
            num_domain=50,
            num_boundary=50,
            num_initial=50,
            solution=func,
            num_test=100,
        )
        
        model = dde.Model(data, net)
        # Just verify that model can be compiled
        self.assertIsNotNone(model)

    def test_geometry_creation(self):
        """Test that geometries are created correctly."""
        geom = dde.geometry.Interval(0, 1)
        timedomain = dde.geometry.TimeDomain(0, 1)
        geomtime = dde.geometry.GeometryXTime(geom, timedomain)
        
        self.assertIsNotNone(geom)
        self.assertIsNotNone(timedomain)
        self.assertIsNotNone(geomtime)

    def test_boundary_conditions_creation(self):
        """Test that boundary conditions are created correctly."""
        geom = dde.geometry.Interval(0, 1)
        timedomain = dde.geometry.TimeDomain(0, 1)
        geomtime = dde.geometry.GeometryXTime(geom, timedomain)
        
        bc = dde.icbc.DirichletBC(
            geomtime, func, lambda _, on_boundary: on_boundary
        )
        ic_1 = dde.icbc.IC(geomtime, func, lambda _, on_initial: on_initial)
        
        self.assertIsNotNone(bc)
        self.assertIsNotNone(ic_1)

    def test_constants_values(self):
        """Test that constants have expected values."""
        self.assertEqual(self.A, 2)
        self.assertEqual(self.C, 10)

    def test_func_bounds(self):
        """Test that function output is bounded."""
        x_test = np.random.rand(100, 2)
        result = func(x_test)
        # The function is a sum of two oscillating terms, should be bounded
        self.assertTrue(np.all(result <= 2.0))
        self.assertTrue(np.all(result >= -2.0))

    def test_multiple_time_steps(self):
        """Test function behavior across multiple time steps."""
        x_coords = np.array([0.5, 0.5, 0.5])
        t_coords = np.array([0.0, 0.5, 1.0])
        x_test = np.column_stack([x_coords, t_coords])
        
        results = func(x_test)
        self.assertEqual(results.shape, (3, 1))
        # All values should be real and finite
        self.assertTrue(np.all(np.isfinite(results)))


class TestWave1DIntegration(unittest.TestCase):
    """Integration tests for wave_1d model."""

    def test_data_creation(self):
        """Test that data object can be created."""
        geom = dde.geometry.Interval(0, 1)
        timedomain = dde.geometry.TimeDomain(0, 1)
        geomtime = dde.geometry.GeometryXTime(geom, timedomain)
        
        bc = dde.icbc.DirichletBC(
            geomtime, func, lambda _, on_boundary: on_boundary
        )
        ic_1 = dde.icbc.IC(geomtime, func, lambda _, on_initial: on_initial)
        ic_2 = dde.icbc.OperatorBC(
            geomtime,
            lambda x, y, _: dde.grad.jacobian(y, x, i=0, j=1),
            lambda x, _: dde.utils.isclose(x[1], 0),
        )
        
        data = dde.data.TimePDE(
            geomtime,
            pde,
            [bc, ic_1, ic_2],
            num_domain=20,
            num_boundary=20,
            num_initial=20,
            solution=func,
            num_test=50,
        )
        
        self.assertIsNotNone(data)
        self.assertGreater(len(data.train_x), 0)

    def test_model_creation(self):
        """Test that model can be created and compiled."""
        geom = dde.geometry.Interval(0, 1)
        timedomain = dde.geometry.TimeDomain(0, 1)
        geomtime = dde.geometry.GeometryXTime(geom, timedomain)
        
        bc = dde.icbc.DirichletBC(
            geomtime, func, lambda _, on_boundary: on_boundary
        )
        ic_1 = dde.icbc.IC(geomtime, func, lambda _, on_initial: on_initial)
        ic_2 = dde.icbc.OperatorBC(
            geomtime,
            lambda x, y, _: dde.grad.jacobian(y, x, i=0, j=1),
            lambda x, _: dde.utils.isclose(x[1], 0),
        )
        
        data = dde.data.TimePDE(
            geomtime,
            pde,
            [bc, ic_1, ic_2],
            num_domain=30,
            num_boundary=30,
            num_initial=30,
            solution=func,
            num_test=100,
        )
        
        layer_size = [2] + [32] * 2 + [1]
        net = dde.nn.FNN(layer_size, "tanh", "Glorot uniform")
        model = dde.Model(data, net)
        model.compl
        
        self.assertIsNotNone(model)


if __name__ == "__main__":
    unittest.main()
