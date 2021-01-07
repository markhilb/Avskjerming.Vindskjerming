import { Component, OnInit, Input } from '@angular/core';

import { Item, Wallmount, Post, Glass } from '../../../models/items.model';
import * as Config from '../../../config.json';

@Component({
  selector: 'app-wall',
  templateUrl: './wall.component.html',
  styleUrls: ['./wall.component.scss'],
})
export class WallComponent implements OnInit {
  @Input() totalWidth: number;
  @Input() globalWidth: number;
  @Input() globalHeight: number;
  @Input() individualWidth: number;
  @Input() individualHeight: number;
  _leftMount: string;
  _rightMount: string;
  _glassType: string;

  items: Item[] = [];
  selectedItem: Item;
  editItem: EditItem;
  modalOpen = false;
  currentWidth = 0;

  constructor() {}

  ngOnInit(): void {}

  @Input() set leftMount(val: string) {
    this._leftMount = val;
    if (this.items.length > 0) {
      if (val === 'post')
        this.items[0] = new Post(this.globalHeight + Config['post']['margin']);
      else if (val === 'wallmount')
        this.items[0] = new Wallmount(
          this.globalHeight + Config['wallmount']['margin'],
        );
    }
  }

  @Input() set rightMount(val: string) {
    this._rightMount = val;
    if (this.items.length > 0) {
      if (val === 'post')
        this.items[this.items.length - 1] = new Post(
          this.globalHeight + Config['post']['margin'],
        );
      else if (val === 'wallmount')
        this.items[this.items.length - 1] = new Wallmount(
          this.globalHeight + Config['wallmount']['margin'],
        );
    }
  }

  @Input() set glassType(val: string) {
    this._glassType = val;
    this.items.forEach((item) => {
      if (item instanceof Glass) item.glassType = val;
    });
  }

  get packageList() {
    return this.items.map((item) => {
      return {
        type: item.constructor.name,
        width: item.width,
        height: item.height,
        secondHeight: item.secondHeight,
        weight: item.weight,
      };
    });
  }

  autoCalculate() {
    this.clear();
    if (!this.totalWidth || this.totalWidth < 10 || this.totalWidth > 9999)
      return;

    // Add the left mount (if there is one)
    if (this._leftMount === 'post') {
      if (!this.addPost(this.globalHeight)) return;
    } else if (this._leftMount === 'wallmount') {
      if (!this.addWallmount(this.globalHeight)) return;
    }

    // Get the width of the right mount (if there is one)
    let rightMountWidth: number;
    if (this._rightMount === 'post')
      rightMountWidth = Config['post']['lastWidth'];
    else if (this._rightMount === 'wallmount')
      rightMountWidth = Config['wallmount']['width'];
    else rightMountWidth = 0;

    // Calculate the number of items to add (minus mounts)
    const width = this.totalWidth - this.currentWidth - rightMountWidth;
    const num = width / (this.globalWidth + Config['post']['width']);

    // Num is floored because another glass and the right mount
    // is added after the loop
    for (let i = 0; i < Math.floor(num); i++) {
      this.addGlass(this.globalWidth, this.globalHeight);
      this.addPost(this.globalHeight);
    }

    this.addGlass(this.globalWidth, this.globalHeight);
    if (this._rightMount === 'post') this.addPost(this.globalHeight);
    else if (this._rightMount === 'wallmount')
      this.addWallmount(this.globalHeight);
  }

  addWallmount(height: number, addMargin = true): boolean {
    if (!this.totalWidth || this.totalWidth < 10 || this.totalWidth > 9999)
      return false;

    // Only add wallmount if the previous item is glass
    // (or this is the first item)
    if (
      this.items.length === 0 ||
      this.items[this.items.length - 1] instanceof Glass
    ) {
      // If adding a wallmount makes the wall too long,
      // try to cut the last glass
      if (
        this.currentWidth + Config['wallmount']['width'] > this.totalWidth &&
        !this.cutGlass(
          this.currentWidth + Config['wallmount']['width'] - this.totalWidth,
        )
      )
        return false;

      this.items.push(
        new Wallmount(
          addMargin ? height + Config['wallmount']['margin'] : height,
        ),
      );
      this.update();
      return true;
    }

    return false;
  }

  addPost(height: number, addMargin = true): boolean {
    if (!this.totalWidth || this.totalWidth < 10 || this.totalWidth > 9999)
      return false;

    // Only add post if the previous item is glass
    // (or this is the first item)
    if (
      this.items.length === 0 ||
      this.items[this.items.length - 1] instanceof Glass
    ) {
      // If adding a post makes the wall too long,
      // try to cut the last glass
      if (
        this.currentWidth + Config['post']['lastWidth'] > this.totalWidth &&
        !this.cutGlass(
          this.currentWidth + Config['post']['lastWidth'] - this.totalWidth,
        )
      )
        return false;

      if (addMargin)
        height +=
          this.items.length === 0 ||
          !this.items[this.items.length - 1].isPolygon
            ? Config['post']['margin']
            : Config['post']['marginPolygon'];

      this.items.push(new Post(height));
      this.update();
      return true;
    }

    return false;
  }

  addGlass(width: number, height: number, secondHeight = -1): boolean {
    if (!this.totalWidth || this.totalWidth < 10 || this.totalWidth > 9999)
      return false;

    if (this.currentWidth < this.totalWidth) {
      if (this.items.length > 0) {
        const lastItem = this.items[this.items.length - 1];
        // Don't add two glasses after each other
        if (lastItem instanceof Glass) return false;

        if (lastItem instanceof Post) {
          // If the last post is no longer last after adding the glass
          if (this.items.length != 1) {
            lastItem.isLast = false;
            this.updateCurrentWidth();
            // If the wall becomes too long from this,
            // undo and don't add glass
            if (this.currentWidth >= this.totalWidth) {
              lastItem.isLast = true;
              this.updateCurrentWidth();
              return false;
            }
          }
        }
      }

      // If the glass is too wide, cut it
      if (this.currentWidth + width > this.totalWidth)
        width = this.totalWidth - this.currentWidth;

      this.items.push(
        new Glass(
          this._glassType,
          width,
          height,
          secondHeight < 0 ? height : secondHeight,
        ),
      );
      this.update();
      return true;
    }

    return false;
  }

  cutGlass(width): boolean {
    if (
      this.items.length > 0 &&
      this.items[this.items.length - 1] instanceof Glass
    ) {
      const glass = this.items.pop();
      if (glass.width <= width) return false;

      const newWidth = glass.width - width;
      this.items.push(
        new Glass(this._glassType, newWidth, glass.height, glass.secondHeight),
      );
      this.update();
      return true;
    }

    return false;
  }

  onEditItem(item: Item) {
    this.selectedItem = item;
    this.editItem = {
      width: item.width,
      height: item.height,
      secondHeight: item.secondHeight,
    };
    this.modalOpen = true;
  }

  editGlass() {
    const secondHalf = this.items.splice(this.items.indexOf(this.selectedItem));
    this.updateCurrentWidth();

    // Add back the new glass
    this.addGlass(
      this.editItem.width,
      this.editItem.height,
      this.editItem.secondHeight,
    );

    if (this.editItem.width >= this.selectedItem.width) {
      // If new glass is wider/same, just add back the old items
      secondHalf.forEach((item) => {
        if (item instanceof Wallmount) this.addWallmount(item.height, false);
        else if (item instanceof Post) this.addPost(item.height, false);
        else this.addGlass(item.width, item.height, item.secondHeight);
      });
    } else {
      // Need to auto calculate the remaining space
      let lastItem: Item;
      if (secondHalf.length > 0) lastItem = secondHalf[secondHalf.length - 1];
      else lastItem = this.items[this.items.length - 1];

      // Calculate number of items to add (minus edges)
      const remainingWidth =
        this.totalWidth - this.currentWidth - lastItem.width;
      const num = remainingWidth / (this.globalWidth + Config['post']['width']);

      for (let i = 0; i < Math.floor(num) + 1; i++) {
        this.addGlass(this.globalWidth, this.globalHeight);
        this.addPost(this.globalHeight);
      }
      this.addGlass(this.globalWidth, this.globalHeight);
      if (lastItem instanceof Wallmount) this.addWallmount(this.globalHeight);
      else if (lastItem instanceof Post) this.addPost(this.globalHeight);
    }
  }

  saveEditItem() {
    if (!this.editItem.height || this.editItem.height <= 0) return;
    if (
      this.selectedItem instanceof Post ||
      this.selectedItem instanceof Wallmount
    )
      this.selectedItem.height = this.editItem.height;
    else if (
      this.editItem.width &&
      this.editItem.height > 0 &&
      this.editItem.secondHeight &&
      this.editItem.secondHeight > 0
    )
      this.editGlass();
    else return;

    this.update();
    this.modalOpen = false;
  }

  deleteItem(item: Item) {
    const index = this.items.indexOf(this.selectedItem);
    const num = index + 1 < this.items.length ? 2 : 1;
    this.items.splice(index, num);
    this.update();

    this.modalOpen = false;
  }

  clear() {
    this.items = [];
    this.currentWidth = 0;
  }

  undo(): boolean {
    const res = this.items.pop();
    if (this.items.length > 0) this.items[this.items.length - 1].isLast = true;
    this.update();
    return res !== undefined;
  }

  updateCurrentWidth = () =>
    (this.currentWidth = this.items.reduce((tot, cur) => tot + cur.width, 0));

  update() {
    this.updateCurrentWidth();
  }

  closeModal = () => (this.modalOpen = false);

  ceil = (a: number): number => Math.ceil(a);

  isWallmount = (item: Item): boolean => item instanceof Wallmount;

  isPost = (item: Item): boolean => item instanceof Post;

  isGlass = (item: Item): boolean => item instanceof Glass;
}

interface EditItem {
  width: number;
  height: number;
  secondHeight: number;
}
