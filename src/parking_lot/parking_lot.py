import logging
from shared_utils.img_preprocess import get_centroid

class Car:
    def __init__(
        self, 
        coords, 
        confidence,
        car_idx,
        owner = None, 
        plate_number = None, 
        occupied_parking_space_idx = None
        ) -> None:
        self.coords = coords
        self.owner = owner
        self.plate_number = plate_number
        self.occupied_parking_space_idx = occupied_parking_space_idx
        self.confidence = confidence
        self.car_idx = car_idx
        self.center_point: tuple[float, float] = get_centroid(coords)

class Cars:
    def __init__(self, cars: list[Car]) -> None:
        self.cars = cars
    
    @classmethod
    def from_list(cls, list_of_cars):

        cars_list = []

        for car_idx, car_info in enumerate(list_of_cars):
            x1, y1, x2, y2, confidence, class_id = car_info
            _car = Car(
                coords=(x1, y1, x2, y2),
                confidence=confidence,
                car_idx=car_idx+1
            )

            cars_list.append(_car)

        return cls(cars_list)

    def to_dict(self):
        return {
            car.car_idx : {
                "coords": car.coords,
                "occupied_parking_space_idx": car.occupied_parking_space_idx,
                "confidence": car.confidence,
                "owner": car.owner,
                "plate_number": car.plate_number,
                "center_point": car.center_point
            }
            for _, car in enumerate(self.cars)
        }

    def add_car(self, car: Car):
        self.cars.append(car)

    def cars_iterator(self):
        for space in self.cars:
            yield space

    def get_cars_count(self):
        return len(self.cars)


class ParkingSpace:
    def __init__(
            self, 
            coords, 
            parking_space_idx: int,
            is_occupied: bool = False, 
            occupied_by_car_idx: int = None
        ) -> None:
        self.is_occupied = is_occupied
        self.coords: tuple[int,int,int,int] = coords
        self.parking_space_idx = parking_space_idx
        self.occupied_by_car_idx = occupied_by_car_idx

    def set_occupied_by(self, car: Car):
        self.is_occupied = True
        self.occupied_by_car_idx = car.car_idx
        car.occupied_parking_space_idx = self.parking_space_idx

    def park_if_inside_space(self, car: Car):
        x1, y1, x2, y2 = self.coords
        center_x, center_y = car.center_point

        if (x2 >= center_x >= x1) and (y2 >= center_y >= y1):
            self.set_occupied_by(car)

class ParkingLot:
    def __init__(self, lots: list[ParkingSpace] = None) -> None:
        self.lots = lots if lots else []
        self.recent_space_idx = 0

    @classmethod
    def from_list(cls, coords_list):
        lot_list = [
            ParkingSpace(
                    space_coords,
                    space_idx
                )
            for space_idx, space_coords in enumerate(coords_list)
        ]
       
        return cls(lot_list)

    @classmethod
    def load_from_dict(cls, parking_lot_info):
        list_of_spaces = [
            ParkingSpace(
                coords=space_info['coords'],
                is_occupied=space_info['is_occupied'],
                parking_space_idx=parking_space_idx,
                occupied_by_car_idx=space_info['occupied_by_car_idx']
            )
            for parking_space_idx, space_info in parking_lot_info
        ]
        return cls(list_of_spaces)

    def to_dict(self):
        return {
            space.parking_space_idx : {
                "coords": space.coords,
                "is_occupied": space.is_occupied,
                "occupied_by_car_idx": space.occupied_by_car_idx
            }
            for _, space in enumerate(self.lots)
        }

    def add_space(self, coords):
        self.lots.append(ParkingSpace(coords, self.recent_space_idx))
        self.recent_space_idx += 1

    def lot_iterator(self):
        for space in self.lots:
            yield space

    def park_car(self, car: Car):
        for space in self.lot_iterator():
            if space.is_occupied:
                continue
            space.park_if_inside_space(car)

            

    def reset_spaces(self):
        for space in self.lot_iterator():
            space.is_occupied, space.occupied_by = False, None

    def summary_dict(self):
        return {
            idx : {
                "coords": space.coords,
                "label": space.is_occupied
            }
            for idx, space in enumerate(self.lots)
        }

    def get_available_spaces_count(self):
        return len([
            lot
            for lot in self.lots
            if lot.is_occupied == False
        ])

    def get_total_spaces_count(self):
        return len(self.lots)
    