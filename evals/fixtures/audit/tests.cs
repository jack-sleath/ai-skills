using Xunit;
using FluentAssertions;
using BookingService.Controllers;
using BookingService.Models;
using BookingService.Services;

namespace BookingService.Tests
{
    public class RoomServiceTests
    {
        [Fact]
        public void CreateRoom_WithValidData_ReturnsCreatedRoom()
        {
            var service = new RoomService(GetDbContext());
            var room = new CreateRoomRequest { Name = "Board Room A", Floor = 3, Capacity = 12, HasVideoConf = true };

            var result = service.CreateRoom(room);

            result.Should().NotBeNull();
            result.Name.Should().Be("Board Room A");
            result.Id.Should().NotBeEmpty();
        }

        [Fact]
        public void CreateRoom_WithDuplicateName_ThrowsConflictException()
        {
            var service = new RoomService(GetDbContext());
            service.CreateRoom(new CreateRoomRequest { Name = "Duplicate", Floor = 1, Capacity = 4 });

            var act = () => service.CreateRoom(new CreateRoomRequest { Name = "Duplicate", Floor = 2, Capacity = 6 });

            act.Should().Throw<ConflictException>().WithMessage("*already exists*");
        }

        [Fact]
        public void GetRooms_FilterByFloor_ReturnsMatchingRooms()
        {
            var service = new RoomService(GetDbContext());
            service.CreateRoom(new CreateRoomRequest { Name = "R1", Floor = 1, Capacity = 4 });
            service.CreateRoom(new CreateRoomRequest { Name = "R2", Floor = 2, Capacity = 6 });
            service.CreateRoom(new CreateRoomRequest { Name = "R3", Floor = 1, Capacity = 8 });

            var result = service.GetRooms(floor: 1);

            result.Should().HaveCount(2);
            result.Should().OnlyContain(r => r.Floor == 1);
        }

        [Fact]
        public void DeleteRoom_WithFutureBookings_ThrowsConflictException()
        {
            var ctx = GetDbContext();
            var service = new RoomService(ctx);
            var room = service.CreateRoom(new CreateRoomRequest { Name = "Busy Room", Floor = 1, Capacity = 4 });

            var bookingService = new BookingService(ctx);
            bookingService.CreateBooking(new CreateBookingRequest
            {
                RoomId = room.Id,
                UserId = Guid.NewGuid(),
                Start = DateTime.UtcNow.AddDays(1),
                End = DateTime.UtcNow.AddDays(1).AddHours(1),
                Title = "Future Meeting"
            });

            var act = () => service.DeleteRoom(room.Id);
            act.Should().Throw<ConflictException>().WithMessage("*future bookings*");
        }
    }

    public class BookingServiceTests
    {
        [Fact]
        public void CreateBooking_WithValidSlot_ReturnsBooking()
        {
            var service = new BookingService(GetDbContext());
            var roomId = SeedRoom(service);
            var request = new CreateBookingRequest
            {
                RoomId = roomId,
                UserId = Guid.NewGuid(),
                Start = DateTime.UtcNow.AddDays(1).Date.AddHours(9),
                End = DateTime.UtcNow.AddDays(1).Date.AddHours(10),
                Title = "Standup",
                Attendees = 5
            };

            var result = service.CreateBooking(request);

            result.Should().NotBeNull();
            result.Title.Should().Be("Standup");
        }

        [Fact]
        public void CreateBooking_WithConflictingSlot_ThrowsConflictException()
        {
            var service = new BookingService(GetDbContext());
            var roomId = SeedRoom(service);
            var baseTime = DateTime.UtcNow.AddDays(1).Date.AddHours(14);

            service.CreateBooking(new CreateBookingRequest
            {
                RoomId = roomId, UserId = Guid.NewGuid(),
                Start = baseTime, End = baseTime.AddHours(1), Title = "First"
            });

            var act = () => service.CreateBooking(new CreateBookingRequest
            {
                RoomId = roomId, UserId = Guid.NewGuid(),
                Start = baseTime.AddMinutes(30), End = baseTime.AddHours(2), Title = "Overlapping"
            });

            act.Should().Throw<ConflictException>().WithMessage("*conflict*");
        }

        [Fact]
        public void CancelBooking_PastBooking_ThrowsBadRequestException()
        {
            var ctx = GetDbContext();
            // Seed a booking in the past via direct DB insert
            var booking = new Booking
            {
                Id = Guid.NewGuid(),
                RoomId = SeedRoom(ctx),
                UserId = Guid.NewGuid(),
                Start = DateTime.UtcNow.AddDays(-2),
                End = DateTime.UtcNow.AddDays(-2).AddHours(1),
                Title = "Old Meeting"
            };
            ctx.Bookings.Add(booking);
            ctx.SaveChanges();

            var service = new BookingService(ctx);
            var act = () => service.CancelBooking(booking.Id);

            act.Should().Throw<BadRequestException>().WithMessage("*past*");
        }

        [Fact]
        public void GetBookings_FilterByDateRange_ReturnsOnlyMatchingBookings()
        {
            var service = new BookingService(GetDbContext());
            var roomId = SeedRoom(service);
            var userId = Guid.NewGuid();

            service.CreateBooking(new CreateBookingRequest { RoomId = roomId, UserId = userId, Start = new DateTime(2025, 3, 10, 9, 0, 0), End = new DateTime(2025, 3, 10, 10, 0, 0), Title = "March meeting" });
            service.CreateBooking(new CreateBookingRequest { RoomId = roomId, UserId = userId, Start = new DateTime(2025, 4, 10, 9, 0, 0), End = new DateTime(2025, 4, 10, 10, 0, 0), Title = "April meeting" });

            var result = service.GetBookings(from: new DateOnly(2025, 3, 1), to: new DateOnly(2025, 3, 31));

            result.Should().HaveCount(1);
            result[0].Title.Should().Be("March meeting");
        }
    }
}
