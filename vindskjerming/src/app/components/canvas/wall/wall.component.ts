import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

import { Item, Wallmount, Post, Glass } from '../../../models/items.model';
import * as Config from '../../../config.json';

@Component({
  selector: 'app-wall',
  templateUrl: './wall.component.html',
  styleUrls: ['./wall.component.scss'],
})
export class WallComponent implements OnInit {
  @Output() packageList = new EventEmitter<any>();

  items: Item[] = [];
  selectedItem: Item;
  editItem: { width: number; height: number; secondHeight: number };

  modalOpen = false;

  _totalWidth: number;
  currentWidth: number;
  _globalWidth: number;
  _globalHeight: number;
  individualWidth: number;
  individualHeight: number;
  _leftMount: string;
  _rightMount: string;
  _glassType: string;

  constructor() {}

  ngOnInit(): void {}

  @Input() set totalWidth(val: number) {
    this._totalWidth = val;
    this.autoCalculate();
  }

  @Input() set globalWidth(val: number) {
    this._globalWidth = val;
    val >= 10 ? this.autoCalculate() : this.clear();
  }

  @Input() set globalHeight(val: number) {
    this._globalHeight = val;
    val >= 10 ? this.autoCalculate() : this.clear();
  }

  @Input() set leftMount(val: string) {
    this._leftMount = val;
    if (val === 'post') this.items[0] = new Post(this._globalHeight);
    else if (val === 'wallmount')
      this.items[0] = new Wallmount(this._globalHeight);
  }

  @Input() set rightMount(val: string) {
    this._rightMount = val;
    if (val === 'post')
      this.items[this.items.length - 1] = new Post(this._globalHeight);
    else if (val === 'wallmount')
      this.items[this.items.length - 1] = new Wallmount(this._globalHeight);
  }

  @Input() set glassType(val: string) {
    this._glassType = val;
    this.items.forEach((item) => {
      if (item instanceof Glass) item.glassType = val;
    });
    this.updatePackageList();
  }

  autoCalculate() {
    this.clear();

    // Add the left mount (if there is one)
    if (this._leftMount === 'post') {
      if (!this.addPost(this._globalHeight)) return;
    } else if (this._leftMount === 'wallmount') {
      if (!this.addWallmount(this._globalHeight)) return;
    }

    // Get the width of the right mount (if there is one)
    let rightMountWidth: number;
    if (this._rightMount === 'post')
      rightMountWidth = Config['post']['lastWidth'];
    else if (this._rightMount === 'wallmount')
      rightMountWidth = Config['wallmount']['width'];
    else rightMountWidth = 0;

    // Calculate the number of items to add (minus mounts)
    const width = this._totalWidth - this.currentWidth - rightMountWidth;
    const num = width / (this._globalWidth + Config['post']['width']);

    // Num is floored because another glass and the right mount
    // is added after the loop
    for (let i = 0; i < Math.floor(num); i++) {
      this.addGlass(this._globalWidth, this._globalHeight);
      this.addPost(this._globalHeight);
    }

    this.addGlass(this._globalWidth, this._globalHeight);
    if (this._rightMount === 'post') this.addPost(this._globalHeight);
    else if (this._rightMount === 'wallmount')
      this.addWallmount(this._globalHeight);
  }

  addWallmount(height: number, addMargin = true): boolean {
    // Only add wallmount if the previous item is glass
    // (or this is the first item)
    if (
      this.items.length === 0 ||
      this.items[this.items.length - 1] instanceof Glass
    ) {
      // If adding a wallmount makes the wall too long,
      // try to cut the last glass
      if (
        this.currentWidth + Config['wallmount']['width'] > this._totalWidth &&
        !this.cutGlass(
          this.currentWidth + Config['wallmount']['width'] - this._totalWidth,
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
    // Only add post if the previous item is glass
    // (or this is the first item)
    if (
      this.items.length === 0 ||
      this.items[this.items.length - 1] instanceof Glass
    ) {
      // If adding a post makes the wall too long,
      // try to cut the last glass
      if (
        this.currentWidth + Config['post']['lastWidth'] > this._totalWidth &&
        !this.cutGlass(
          this.currentWidth + Config['post']['lastWidth'] - this._totalWidth,
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
    if (this.currentWidth < this._totalWidth) {
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
            if (this.currentWidth >= this._totalWidth) {
              lastItem.isLast = true;
              this.updateCurrentWidth();
              return false;
            }
          }
        }
      }

      // If the glass is too wide, cut it
      if (this.currentWidth + width > this._totalWidth)
        width = this._totalWidth - this.currentWidth;

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
        this._totalWidth - this.currentWidth - lastItem.width;
      const num =
        remainingWidth / (this._globalWidth + Config['post']['width']);

      for (let i = 0; i < Math.floor(num) + 1; i++) {
        this.addGlass(this._globalWidth, this._globalHeight);
        this.addPost(this._globalHeight);
      }
      this.addGlass(this._globalWidth, this._globalHeight);
      if (lastItem instanceof Wallmount) this.addWallmount(this._globalHeight);
      else if (lastItem instanceof Post) this.addPost(this._globalHeight);
    }
  }

  saveEditItem() {
    if (
      this.selectedItem instanceof Post ||
      this.selectedItem instanceof Wallmount
    )
      this.selectedItem.height = this.editItem.height;
    else this.editGlass();

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

  updatePackageList() {
    this.packageList.emit(
      this.items.map((item) => {
        return {
          type: item.constructor.name,
          width: item.width,
          height: item.height,
          secondHeight: item.secondHeight,
          weight: item.weight,
        };
      }),
    );
  }

  update() {
    this.updateCurrentWidth();
    this.updatePackageList();
  }

  closeModal = () => (this.modalOpen = false);

  ceil = (a: number): number => Math.ceil(a);

  isWallmount = (item: Item): boolean => item instanceof Wallmount;

  isPost = (item: Item): boolean => item instanceof Post;

  isGlass = (item: Item): boolean => item instanceof Glass;
}
