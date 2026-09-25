from tuova_machinedata_processing import postgres
from tuova_machinedata_processing import data_processor

def main():
    # TODO:

    # here's the plan:
    data = postgres.get_data()
    new_data = data_processor.transform(data)
    postgres.update_data(new_data)


if __name__ == "__main__":
    main()
