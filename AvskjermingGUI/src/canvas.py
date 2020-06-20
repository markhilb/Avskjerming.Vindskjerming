import tkinter
from tkinter import messagebox
from tkinter.simpledialog import askstring
from decimal import Decimal
from items import Wallmount, Post, Glass, LengthBar, GlassPolygon
from config import CANVAS_LEFT_START, POST_WIDTH, POST_LAST_WIDTH, \
                   WALLMOUNT_WIDTH, POST_MARGIN_ABOVE_GLASS, \
                   POST_MARGIN_ABOVE_GLASSPOLYGON, WALLMOUNT_MARGIN_ABOVE_GLASS, \
                   CANVAS_SPACE_BETWEEN_WALLS


class Thing:
    def __init__(self, canvas):
        self.canvas = canvas
        self.items = []
        self.base_xpos = CANVAS_LEFT_START
        self.current_xpos = CANVAS_LEFT_START
        self.current_width = Decimal("0")
        self.length_bar = LengthBar(canvas)


    @property
    def is_empty(self):
        return len(self.items) == 0


    def auto_calculate(self, total_width, width, height, left, right):
        self.clear()

        # Add the leftmost item (if there is one)
        if left is Post:
            if not self.add_post(total_width, height):
                return
        elif left is Wallmount:
            if not self.add_wallmount(total_width, height):
                return

        # Add the rightmost item (if there is one),
        # and save its width
        if right is Post:
            right_item_width = POST_LAST_WIDTH
            right_item_add_func = self.add_post
        elif right is Wallmount:
            right_item_width = WALLMOUNT_WIDTH
            right_item_add_func = self.add_wallmount
        else:
            right_item_width = 0
            right_item_add_func = lambda x, y: None

        # Calculate the number of items to add (minus the edges)
        total_width_minus_edges = total_width - self.current_width - right_item_width
        num =  total_width_minus_edges / (width + POST_WIDTH)

        # Num is floored because another glass and the right item
        # needs to be added after the loop
        for _ in range(int(num)):
            self.add_glass(total_width, width, height)
            self.add_post(total_width, height)

        self.add_glass(total_width, width, height)
        right_item_add_func(total_width, height)


    def add_wallmount(self, total_width, height, add_margin=True):
        # Don't add wallmount if the last item is not glass
        # (unless this is the first item)
        if len(self.items) > 0 and not isinstance(self.items[-1], Glass):
            return False

        # Try to cut the last glass if adding a wallmount makes it too long
        if self.current_width + WALLMOUNT_WIDTH > total_width:
            if not self.cut_glass(self.current_width + WALLMOUNT_WIDTH - total_width):
                return False

        if add_margin:
            wallmount = Wallmount(
                self.canvas, self.current_xpos, height + WALLMOUNT_MARGIN_ABOVE_GLASS
            )
        else:
            wallmount = Wallmount(self.canvas, self.current_xpos, height)

        self.items.append(wallmount)
        self.update()
        return True


    def add_post(self, total_width, height, add_margin=True):
        # Don't add post if the last item is not glass
        # (unless this is the first item)
        if len(self.items) > 0 and not isinstance(self.items[-1], Glass):
            return False

        # Try to cut the last glass if adding a wallmount makes it too long
        if self.current_width + POST_LAST_WIDTH > total_width:
            if not self.cut_glass((self.current_width + POST_LAST_WIDTH) - total_width):
                return False

        if add_margin:
            if len(self.items) == 0 or not isinstance(self.items[-1], GlassPolygon):
                height += POST_MARGIN_ABOVE_GLASS
            else:
                height += POST_MARGIN_ABOVE_GLASSPOLYGON

        post = Post(self.canvas, self.current_xpos, height, True)
        self.items.append(post)
        self.update()
        return True


    def add_glass(self, total_width, width, height, second_height=-1):
        if self.current_width >= total_width:
            return False

        if len(self.items) > 0:
            # Don't add two glasses after each other
            if isinstance(self.items[-1], Glass):
                return False

            # If the previous item is a post
            if self.items[-1] is Post:
                # If the last post is no longer last after adding the glass,
                # set is_last to false, and update the canvas
                if len(self.items) != 1:
                    self.items[-1].is_last = False
                    self.update()
                    # If this becomes too long from doing this,
                    # set is_last back to true, and don't add the class
                    if self.current_width >= total_width:
                        self.items[-1].is_last = True
                        self.update()
                        return False

        # If the glass is too wide, cut it
        if self.current_width + width > total_width:
            width = total_width - self.current_width

        if second_height == -1:
            glass = Glass(self.canvas, self.current_xpos, width, height)
        else:
            glass = GlassPolygon(
                self.canvas, self.current_xpos, width, height, second_height
            )

        self.items.append(glass)
        self.update()
        return True


    def cut_glass(self, width):
        # Can't cut a glass that is not there
        if len(self.items) == 0:
            return False

        # Can't cut something that is not glass
        if not isinstance(self.items[-1], Glass):
            return False

        glass = self.items.pop()

        # Can't cut more than the glass' width
        if glass.width <= width:
            self.items.append(glass)
            return False

        new_width = glass.width - width
        self.update()
        if isinstance(glass, GlassPolygon):
            new_glass = GlassPolygon(
                self.canvas,
                self.current_xpos,
                new_width, glass.height, glass.second_height
            )
        else:
            new_glass = Glass(self.canvas, self.current_xpos, new_width, glass.height)

        self.items.append(new_glass)
        glass.delete()
        self.update()
        return True


    def edit_glass(self, glass_id, total_width, width, height):
        for i, item in enumerate(self.items):
            if item.id is glass_id:
                # Split the list where the glass is
                second_half = self.items[i+1:]
                self.items = self.items[:i+1]

                # Delete the glass to be edited
                old_glass = self.items.pop()
                old_glass.delete()
                self.update()

                # Add new glass back with the edited size
                self.add_glass(total_width, width, height)

                # If the edited glass is made wider or the same
                if width >= old_glass.width and len(second_half) > 0:
                    # Add back the rest of the items
                    for itm in second_half:
                        if isinstance(itm, Wallmount):
                            self.add_wallmount(total_width, itm.height, False)
                        elif isinstance(itm, Post):
                            self.add_post(total_width, itm.height, False)
                        else:
                            self.add_glass(total_width, itm.width, itm.height)

                        itm.delete()

                # If the edited glass is made smaller
                else:
                    # Delete the old items
                    [x.delete() for x in second_half]

                    # Get the size of the glasses to fill up the rest of the space
                    if not (auto_width := self.canvas.parent.get_auto_glass_width()) or \
                            not (auto_height := self.canvas.parent.get_auto_glass_height()):
                        return

                    # Find out what the last item is
                    if second_half:
                        last_item = second_half[-1]
                    else:
                        last_item = self.items[-1]

                    # Calculate the number of items to add (minus the edges)
                    remaining_width = total_width - self.current_width - last_item.width
                    num = remaining_width / (auto_width + POST_WIDTH)

                    # Num is floored because another glass and the right item
                    # needs to be added after the loop
                    for _ in range(int(num) + 1):
                        self.add_glass(total_width, auto_width, auto_height)
                        self.add_post(total_width, auto_height)

                    self.add_glass(total_width, auto_width, auto_height)
                    if isinstance(last_item, Post):
                        self.add_post(total_width, auto_height)
                    elif isinstance(last_item, Wallmount):
                        self.add_wallmount(total_width, auto_height)

                return True

        return False


    def delete_glass(self, glass_id):
        for i, item in enumerate(self.items):
            if item.id is glass_id:
                # Delete the glass
                item.delete()
                self.items.remove(item)

                # If there is a post/wallmount after the glass, delete it too
                if len(self.items) > i:
                    next_item = self.items[i]
                    if isinstance(next_item, Post) or isinstance(next_item, Wallmount):
                        next_item.delete()
                        self.items.remove(next_item)

                self.redraw_items()
                self.update()
                return True

        return False


    def edit_post_or_wallmount(self, item_id, height):
        for i, item in enumerate(self.items):
            if item.id is item_id:
                item.delete()
                if isinstance(item, Post):
                    self.items[i] = Post(self.canvas, item.xpos, height, True)
                elif isinstance(item, Wallmount):
                    self.items[i] = Wallmount(self.canvas, item.xpos, height)
                else:
                    return False

                return True

        return False


    def delete_post_or_wallmount(self, item_id):
        for i, item in enumerate(self.items):
            if item.id is item_id:
                # Delete the item
                item.delete()
                self.items.remove(item)

                # If there is a glass after the item, delete it too
                if len(self.items) > i:
                    next_item = self.items[i]
                    if isinstance(next_item, Glass):
                        next_item.delete()
                        self.items.remove(next_item)

                self.redraw_items()
                self.update()
                return True

        return False


    def redraw_items(self):
        old_items = self.items
        total_width = self.current_width
        self.items = []
        self.current_width = Decimal("0")
        self.current_xpos = self.base_xpos

        for item in old_items:
            if isinstance(item, Wallmount):
                self.add_wallmount(total_width, item.height, False)
            elif isinstance(item, Post):
                self.add_post(total_width, item.height, False)
            else:
                self.add_glass(total_width, item.width, item.height)

            item.delete()


    def clear(self):
        for item in self.items:
            item.delete()

        self.items.clear()
        self.current_width = Decimal("0")
        self.current_xpos = self.base_xpos
        self.length_bar.update(self.current_width, self.current_xpos, self.base_xpos)


    def update(self):
        self.current_width = Decimal("0")
        self.current_xpos = self.base_xpos
        for item in self.items:
            self.current_width += item.width
            self.current_xpos += item.display_width

        self.length_bar.update(self.current_width, self.current_xpos, self.base_xpos)


class Canvas(tkinter.Canvas):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, bg="white", highlightthickness=0)
        self.left_thing = Thing(self)
        self.right_thing = Thing(self)


    def auto_calculate(self, total_width_l, total_width_r, width, height):
        left_item = self.parent.get_left_item()
        right_item = self.parent.get_right_item()
        if total_width_r:
            self.left_thing.auto_calculate(
                total_width_l, width, height, left_item, Post
            )

            self.right_thing.base_xpos = (self.left_thing.current_xpos +
                                          CANVAS_SPACE_BETWEEN_WALLS)
            self.right_thing.auto_calculate(
                total_width_r, width, height, None, right_item
            )
        else:
            self.right_thing.clear()
            self.left_thing.auto_calculate(
                total_width_l, width, height, left_item, right_item
            )


    def add_wallmount(self, total_width_l, total_width_r, height):
        if total_width_r:
            # If the right thing is not empty, then the wallmount is added there
            if not self.right_thing.is_empty:
                self.right_thing.add_wallmount(total_width_r, height)
            # If the right thing is empty, try to add to the left thing
            else:
                # If the wallmount can't be added to the left thing,
                # add it to the right thing anyway
                if not self.left_thing.add_wallmount(total_width_l, height):
                    self.right_thing.add_wallmount(total_width_r, height)
        else:
            self.left_thing.add_wallmount(total_width_l, height)


    def add_post(self, total_width_l, total_width_r, height):
        if total_width_r:
            # If the right thing is not empty, then the post is added there
            if not self.right_thing.is_empty:
                self.right_thing.add_post(total_width_r, height)
            # If the right thing is empty, try to add to the left thing
            else:
                # If the post can't be added to the left thing,
                # add it to the right thing anyway
                if not self.left_thing.add_post(total_width_l, height):
                    self.right_thing.add_post(total_width_r, height)
        else:
            self.left_thing.add_post(total_width_l, height)


    def add_glass(self, total_width_l, total_width_r, width, height, second_height=-1):
        if total_width_r:
            # If the right thing is not empty, then the glass is added there
            if not self.right_thing.is_empty:
                self.right_thing.add_glass(total_width_r, width, height, second_height)
            # If the right thing is empty, try to add to the left thing
            else:
                # If the glass can't be added to the left thing,
                # add it to the right thing anyway
                if not self.left_thing.add_glass(total_width_r, width, height, second_height):
                    self.right_thing.add_glass(total_width_r, width, height, second_height)
        else:
            self.left_thing.add_glass(total_width_l, width, height, second_height)


    def update(self):
        self.left_thing.update()
        self.right_thing.update()


    def clear(self):
        self.left_thing.clear()
        self.right_thing.clear()


    def undo(self):
        # Figure out which list to undo from
        if self.right_thing.is_empty:
            items = self.left_thing.items
        else:
            items = self.right_thing.items

        if not items:
            return

        # Remove last item
        item = items.pop()
        item.delete()

        # If the last iitem  is now a post, set is_last to true
        if len(items) > 0 and isinstance(items[-1], Post):
            items[-1].is_last = True

        self.update()


    def edit_glass(self, glass_id, width, height):
        if list(filter(lambda item: item.id == glass_id, self.left_thing.items)):
            self.left_thing.edit_glass(
                glass_id, self.parent.get_total_length_l(), width, height
            )
        else:
            self.right_thing.edit_glass(
                glass_id, self.parent.get_total_length_r(), width, height
            )

        self.parent.update_packaging_list()


    def delete_glass(self, glass_id):
        if list(filter(lambda item: item.id == glass_id, self.left_thing.items)):
            self.left_thing.delete_glass(glass_id)
        else:
            self.right_thing.delete_glass(glass_id)

        self.parent.update_packaging_list()


    def edit_post_or_wallmount(self, item_id, height):
        if list(filter(lambda item: item.id == item_id, self.left_thing.items)):
            self.left_thing.edit_post_or_wallmount(item_id, height)
        else:
            self.right_thing.edit_post_or_wallmount(item_id, height)

        self.parent.update_packaging_list()


    def delete_post_or_wallmount(self, item_id, height):
        if list(filter(lambda item: item.id == item_id, self.left_thing.items)):
            self.left_thing.delete_post_or_wallmount(item_id)
        else:
            self.right_thing.delete_post_or_wallmount(item_id)

        self.parent.update_packaging_list()


    def get_packaging_list(self):
        pl = {}
        pl["Weight"] = Decimal("0")
        for item in self.left_thing.items + self.right_thing.items:
            # Get the map for this type of item, and create an empty one if it does not exist.
            # Increments the value for this items's size, or initializes it if does not exist.
            if isinstance(item, GlassPolygon):
                pl["Skrå glass"][f"{item.width}x{item.height}x{item.second_height}"] = (
                    pl.setdefault("Skrå glass", {})
                      .setdefault(f"{item.width}x{item.height}x{item.second_height}", 0) + 1
                 )
            elif isinstance(item, Glass):
                pl["Glass"][f"{item.width}x{item.height}"] = (
                    pl.setdefault("Glass", {})
                      .setdefault(f"{item.width}x{item.height}", 0) + 1
                )
            elif isinstance(item, Post):
                pl["Stolpe"][f"{item.height}"] = (
                    pl.setdefault("Stolpe", {})
                      .setdefault(f"{item.height}", 0) + 1
                )
            elif isinstance(item, Wallmount):
                pl["Veggskinne"][f"{item.height}"] = (
                    pl.setdefault("Veggskinne", {})
                      .setdefault(f"{item.height}", 0) + 1
                )

            # Add the items weight to the map
            w = item.weight
            pl["Weight"] += w[0] + w[1]

        return pl

