from app import create_app
from seeds.seed_parameter_master import seed_parameters

app = create_app()

with app.app_context():
    seed_parameters()

print("Production parameter seed completed.")